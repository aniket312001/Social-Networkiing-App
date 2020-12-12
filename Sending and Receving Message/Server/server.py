from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person 

# GLOBAL CONSTANTS  
HOST = 'localhost'
PORT = 8720
BUFSIZE = 512 # maximum length of text to be send
ADDR = (HOST,PORT)
MAX_CONNECTION = 10

# GLOBAL VARIABLE
persons = []
SERVER = socket(AF_INET,SOCK_STREAM) # Creating Server
SERVER.bind(ADDR)   # Binding the Address to run the server



def broadcast(msg, name):
    """
    Send new messages for all clients 
    param msg : bytes('utf8)
    param name : str
    return : None 
    """

    for person in persons:
        client = person.client
        try:
            client.send(bytes(name ,'utf8') +msg)
        except Exception as e:
            print(f'[EXCEPTION] 4: {e}')




def client_communication(person):
    """
    Thread to handle all messages from clients
    param Person: Person
    return None
    """

    client = person.client

    # first message received is always the person name
    name = client.recv(BUFSIZE).decode('utf8')
    person.set_name(name)

    msg = bytes(f'{name} has join the chat !!','utf8')
    broadcast(msg, "")  # broadcast Welcome Message

    while True:  # Wait for any messages from person
        try:
            msg = client.recv(BUFSIZE)  

            if msg == bytes("{quit}","utf8"): # if message is quit disconnect client
                client.close()
                persons.remove(person)
                broadcast(bytes(f'{name} has left the chat....','utf8'),"")
                print(f'[DISCONNECTED]: {name} disconnected')
                break
            else:    # otherwise send messages to all other clients
                broadcast(msg, name+': ')
                print(f'{name}: ', msg.decode('utf8'))

        except Exception as e:
            print(f'[EXCEPTION] 2: {e}')
            exit(0)




def wait_for_connections():

    """ 
    Wait for connection from new clients,start new Thread once connected 
    param SERVER : SOCKET
    return : None
    """

    while True:
        try:
            client,addr = SERVER.accept()  # Accpting client to join
            person = Person(addr,client)  # create a new person for connection 
            persons.append(person)
            print(f'[CONNECTION] {addr} connected to the server at {time.time()}')
            Thread(target=client_communication,args=(person,)).start()  # Creating thread for client communications
        except Exception as e:
            print(F'[EXCEPTION] 3: {e}')
            break

    print("SERVER CRASHED")
 




if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTION)  # Total connection can join
    print("Waiting For Connections...") 
    ACCEPT_THREAD = Thread(target=wait_for_connections) # Start new Thread and Making Thread for joining new connections
    ACCEPT_THREAD.start() # Starting the Server
    ACCEPT_THREAD.join()
    SERVER.close()  

