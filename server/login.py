from tkinter import *
from server.users import Users

'''
responsible for the first screen - the login for each user
'''
class Login(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.user = Users()


    def check_in_sql(self):
        # if user exists in database and password and username match
        # then return true else return false
        print("checking")
        try:
            # check if username and password in database
            answer = self.user.check_user_and_pass(self.username, self.password)
            if answer:
                print(f"{self.username} logged in successfully")
            else:
                print(f"{self.username} failed login attempt ")
            return answer

        except:
            print(f"{self.username} failed login attempt ")
            return False


