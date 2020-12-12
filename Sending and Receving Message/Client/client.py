from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread,Lock
import time


class Client:
    """
    For communication with server
    """

    # GLOBAL CONSTANTS  
    HOST = 'localhost'
    PORT = 8720
    ADDR = (HOST,PORT)
    BUFSIZE = 512 

    def __init__(self,name):
        """
        Init object and send name to server
        param name : str     
        """

        self.client_socket = socket(AF_INET,SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []      
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_messages(name)
        self.lock = Lock()    


    def receive_messages(self):
        """
        receive messages from server
        return : None 
        """

        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZE).decode()
                self.lock.acquire()  # make sure memory is safe to access
                self.messages.append(msg)
                self.lock.release()

            except Exception as e:
                print(f'[EXCEPTION] 1: {e}')
                break


        
    def send_messages(self,msg):
        """
        send messages to server
        param msg: str
        return : None 
        """
        try:
            self.client_socket.send(bytes(msg,'utf8'))

            if msg == '{quit}':
                self.client_socket.close()
        except Exception as e:
            self.client_socket = socket(AF_INET,SOCK_STREAM)
            self.client_socket.connect(self.ADDR)
            print(e)


    def get_messages(self):
        """
        Returns list of messages
        return : list[str]
        """
        
        messages_copy = self.messages[:]
        # Make sure memory safe to access
        self.lock.acquire()
        self.messages = []
        self.lock.release()
        return messages_copy


    

    def disconnect(self):
        """
        send messages quit
        return : None
        """
        self.send_messages("{quit}")


    