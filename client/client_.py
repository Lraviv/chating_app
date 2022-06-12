'''
handles connection to server
'''

import socket
import threading
from get_ip_addresses import address
import json
import sys, os

# protocol: action||msg
class Client(object):
    def __init__(self, msg):
        self.msg = msg

    def send_msg(self):
        # send msg to client
        data = json.loads(self.msg)
        sock.sendall(str.encode(data))

    def identify_func(self):
        # handle function identification
        num = 0
        # get from protocol number of function to do
        if num ==1:
            pass
        pass

# Get server ip and port
net = address()
serverIP = net.get_server_ip()
port = net.get_port()


def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(32)
            print(str(data.decode("utf-8")))
        except:
            print("You have been disconnected from the server")
            signal = False
            break



#Attempt connection to server
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((serverIP, port))
except:
    print("Could not make a connection to the server")
    input("Press enter to quit")
    sys.exit(0)


# Create new thread to wait for data
receiveThread = threading.Thread(target=receive, args=(sock, True))
receiveThread.start()


## Send data to server
# while True:
#    json.loads(msg)
#    sock.sendall(str.encode(msg))
