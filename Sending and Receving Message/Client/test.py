from client import Client
import time
from threading import Thread

c1 = Client("Aniket")   # this parameter will set the name
c2 = Client("Sam")



def update_messages():
    """
    updates the local list of messages
    :return: None
    """
    msgs = []
    run = True
    while run:
        time.sleep(0.1)  # update every 1/10 of a second
        new_messages = c1.get_messages()  # get any new messages from client
        msgs.extend(new_messages)  # add to local list of messages

        for msg in new_messages:  # display new messages
            print(msg)

            if msg == "{quit}":
                run = False
                break


Thread(target=update_messages).start()




c1.send_messages("Hello")
time.sleep(3)

c2.send_messages("Bye")
time.sleep(3)

c1.send_messages("Why")
time.sleep(4)

c2.send_messages("Sleeping")
time.sleep(2)


c2.disconnect()
time.sleep(1)
c1.disconnect()


