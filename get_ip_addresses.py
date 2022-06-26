# get the server and client ip and port from txt file
import os

class address(object):
    def __init__(self):
        #TODO - change to relative path
        #self.file = r'/pythonProject1/network_data.txt'

        #self.data_arr = self.sep_data()  # stores all data [serverIP, ClientIP, port]
        self.data_arr = ['127.0.0.1', '0.0.0.0', 8448]
        #self.check_()

    def get_server_ip(self):
        # return the server ip from the file
        print("serverIP: ",  self.data_arr[0])
        return self.data_arr[0]

    def get_client_ip(self):
        # get client ip from file
        return self.data_arr[1]

    def get_port(self):
        # return port from file
        return int(self.data_arr[2])

    def check_(self):
        # check if the data in file is valid
        if len(self.data_arr) == 3:  # check if array has 3 elements
            print("data in file is valid")
        else:
            print("data in file is invalid")

    def sep_data(self):
        # separate the usable data [ips,port] in file from its text
        data_arr = []
        # open the file of the network details
        with open(self.file, 'r') as f:
            for line in f:
                stripped_line = line.strip()
                line_arr = stripped_line.split(': ')
                data_arr.append(line_arr[1])   # get second item from array (the network data)
            f.close()

        print(data_arr)
        return data_arr
