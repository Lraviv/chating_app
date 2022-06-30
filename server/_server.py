import hashlib
import socket
import os
from _thread import *
from server import login
from server import signup
from users import Users
from server import RSA
from get_ip_addresses import address as ad


class s():
    def __init__(self):
        self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        a = ad()
        host = a.get_client_ip()
        port = int(a.get_port())
        (self.pub_key,priv) = RSA.generate_keys()
        print("public key is "+str(self.pub_key))
        ThreadCount = 0
        self.clients = {}   # dict of client_name:client_conn
        self.users_online = []  # all users that are currently online
        self.client_num = 0

        try:
            self.ServerSocket.bind((host, port))
        except socket.error as e:
            print(str(e))

        print('Waiting for a Connection..')
        self.ServerSocket.listen(10)  # atmost conncetions

        while True:
            Client, self.address = self.ServerSocket.accept()
            self.client_num += 1
            print('Connected to: ' + self.address[0] + ':' + str(self.address[1]))
            start_new_thread(self.threaded_client, (Client,))
            ThreadCount += 1
            print('Thread Number: ' + str(ThreadCount))

        self.ServerSocket.close()

    def threaded_client(self, connection):
        # we need to create a function that handles requests from the individual client by a thread
        self.clients[self.address] = connection
        self.connection = connection
        # sending public key to new user
        self.connection.send(str.encode("01|" + str(self.pub_key)))
        print(f"sending the public key {str(self.pub_key)}")
        while True:
            try:
                data = connection.recv(2048)  # receive data from client
                data = data.decode()
                if data != None:
                    print("[CLIENT]: ", data)
                    res = self.decrypt(data)
                    self.data_to_send(res)
            except:
                user = self.get_username(self.connection)
                try:
                    self.users_online.remove(user)
                    del self.clients[user]
                    print(f"{user} closed connection")
                    break
                except:
                    break
        connection.close()

    def data_to_send(self, response):
        # send response
        if response:
            response = "True"
        elif not response:
            response = "False"
        print(f"[SERVER] {response} as {type(response)}")
        self.connection.send(str.encode(response))

    def commit_action(self, id, data):
        # commit action of id IN SERVER 
        response = "False"
        if id == "00":  # send rsa key
            pass
        elif id == "01":
            pass
        elif id == "02":  # login
            # check if data received in database
            data = data.split("+")
            data[1] = self.hash_password(data[1])   # hash the password
            user = login.Login(data[0], data[1])
            response = user.check_in_sql()
            if response:
                self.users_online.append(data[0])
                try:
                    self.clients[data[0]] = self.clients.pop(self.address)
                    print(self.clients)
                except Exception as e:
                    pass

        elif id == "03":    # sign up
            data = data.split("+")
            data[1] = self.hash_password(data[1])   # hash the password
            user = signup.sign(data[0], data[1], data[2])
            response = user.create_a_user()
            if response:
                self.clients[data[0]] = self.clients.pop(self.address)
            print(response)

        elif id == "04":    # client wants to send message
            try:
                data = data.split("+")  # target+data
                if data[0] in self.users_online:
                    print(f"{self.address} sending {data[1]} to {data[0]}")
                    target = self.clients.get(data[0], )
                    print(target)
                    username = self.get_username(self.connection)
                    target.send(str.encode("00|"+username+"+"+data[1]))
                else:
                    print(f"{data[0]} not online")

            except:
                print("no such user")

        elif id == "05":    #client wants to add user
            user = Users()
            try:
                username = self.get_username(self.connection)
                if data in self.users_online:
                    response = user.is_username_exist(username, data)
                    print(f"{username} adding {username} is {response}")
                else:
                    response = "False"
            except:
                response = 'False'
                print("[EXCEPTION] can't find user")
        else:
            print("not matching")

        return response  # return the response to client

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

    def get_username(self, connection):
        # return requested connection's username
        keys = list(self.clients.keys())
        values = list(self.clients.values())
        username = keys[values.index(connection)]
        return username

    def hash_password(self, password):
        # hash the given data
        try:
            hashed = str(hashlib.sha256(password.encode()).hexdigest())
            #hashed = str(hash(password))
            print("hashed password is " + hashed)
            return hashed
        except Exception as e:
            print(f"[HASH ERROR] {e}")
            return password


s()