from server import login
from server import signup

class protocl():
    def __init__(self):
        pass

    def sort(self, action,data):
        # get data in protocol
        if action == "ip":  # ip code is 00
            id = "00"
        elif action == "key":
            id = "01"
        elif action == "login":   # login code is 02
            id = "02"
        elif action == "signup":
            id = "03"
        elif action == "send_msg":
            id = "04"
        else:
            id = -1

    def encrypt(self, id, data):
        # get msg in format  id|size|data
        size = len(data.encode())
        new_data = (id + "|" + str(size) + "|" + str(data))
        print(new_data)


class server_protocol():
    def __init__(self):
        pass

    def desort(self, id, data):
        # commit action of id
        print(id)
        if id == "00":
            pass
        elif id == "01":
            pass
        elif id == "02":  # login
            data = data.split("+")
            print(data)
            user = login.Login(data[0], data[1])
            response = user.check_in_sql()
            print(response)

        elif id == "03":
            data = tuple(data)
            signup.sign(data)
        else:
            print("not matching")

        return response

    def decrypt(self,data):
        new_data = data.split("|")
        res = self.desort(new_data[0], new_data[2])
        return res

prot = server_protocol()
prot.decrypt("02|1024|lihi+111")