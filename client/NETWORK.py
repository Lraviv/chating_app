'''
handles the network
'''
import socket
import json

class Network(object):
    def __init__(self, data):
        self.temp = json.loads(data)

    def send(self):
        # send data to server
        pass

    def receive(self):
        # receive data
        pass