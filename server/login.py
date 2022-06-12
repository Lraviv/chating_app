from tkinter import *
from users import Users

'''
responsible for the first screen - the login for each user
'''
class Login(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password


    def check_in_sql(self):
        # if user exists in database and password and username match
        # then return true else return false

        try:
            # check if username and password in database
            answer = Users.check_user_and_pass(self.username, self.password)
            print(f"{self.username} logged in successfully")
            return True

        except:
            print(f"{self.username} failed login attempt ")
            return False


