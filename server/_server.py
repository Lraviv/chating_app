import socket
import os
from _thread import *
from server import login
from server import signup
from get_ip_addresses import address as ad

class s():
    def __init__(self):
        self.ServerSocket = socket.socket()
        a = ad()
        host = a.get_client_ip()
        port = int(a.get_port())
        ThreadCount = 0
        self.adds = {}
        self.clients = {}   # dict of client_name:client_conn
        self.client_num = 0

        try:
            self.ServerSocket.bind((host, port))
        except socket.error as e:
            print(str(e))

        print('Waiting for a Connection..')
        self.ServerSocket.listen(10)  # atmost conncetions

        while True:
            Client, address = self.ServerSocket.accept()
            self.add = address
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
        self.clients[self.add] = self.connection
        while True:
            data = connection.recv(2048)  # receive data from client
            data = data.decode()
            print("[CLIENT]: ", data)
            res = self.decrypt(data)
            self.data_to_send(res)
        connection.close()


    def data_to_send(self, response):
        # gets what to send to client
        # send response
        # response = self.encrypt(response)
        print(f"sending {response}")
        self.connection.send(str.encode(response))

    def commit_action(self, id, data):
        # commit action of id IN SERVER 
        response = -1
        print(id)
        if id == "00":
            pass
        elif id == "01":
            pass
        elif id == "02":  # login
            # check if data received in database
            data = data.split("+")
            user = login.Login(data[0], data[1])
            response = user.check_in_sql()
            if response:
                response = "True"
                self.clients[data[0]] = self.clients.pop(self.add)
                print(self.clients)

        elif id == "03":    # sign up
            data = data.split("+")
            user = signup.sign(data[0], data[1], data[2])
            response = user.create_a_user()
            if response:
                response = "True"
                self.clients[data[0]] = self.clients.pop(self.add)
            print(response)

        elif id == "04":    # client wants to send message
            data = data.split("+")  # target+data
            print(f"{self.add} sending {data[1]} to {data[0]}")
            # send data[1] to data[0]
            #target = self.clients[data[0]]
        else:
            print("not matching")


        # return response to client
        print(response)
        return response

    def decrypt(self, data):
        # first encrypt msg then commit action
        new_data = data.split("|")
        id, data = new_data[0], new_data[2]
        res = self.commit_action(id,data)
        return res

    def encrypt(self, id, data):
        # get msg in format  id|size|data before sending
        size = len(data.encode())
        new_data = (id + "|" + str(size) + "|" + str(data))
        return new_data

s()