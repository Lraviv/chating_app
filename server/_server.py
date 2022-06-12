import socket
import os
from _thread import *

class s():
    def __init__(self):
        self.ServerSocket = socket.socket()
        host = '127.0.0.1'
        port = 8448
        ThreadCount = 0
        self.adds = {}
        self.client_num = 0


        try:
            self.ServerSocket.bind((host, port))
        except socket.error as e:
            print(str(e))

        print('Waiting for a Connection..')
        self.ServerSocket.listen(10)  # atmost conncetions

        while True:
            Client, address = self.ServerSocket.accept()
            self.adds[self.client_num] = address[0]
            self.client_num+=1
            print(self.adds)
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(self.threaded_client, (Client,))
            ThreadCount += 1
            print('Thread Number: ' + str(ThreadCount))

        self.ServerSocket.close()

    def threaded_client(self, connection):
        # we need to create a function that handles requests from the individual client by a thread
        self.connection = connection
        connection.send(str.encode('Welcome to the Server'))
        while True:
            data = connection.recv(2048)  # receive data from client
            print("client said - ", data.decode())
            self.data_to_send()
        connection.close()


    def data_to_send(self):
        # gets what to send to client
        # send response
        data = "received"
        reply = 'Server:' + data
        print(f"sending {reply}")
        # if not data:
        #    break
        self.connection.sendall(str.encode(reply))


s()