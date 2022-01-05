from tkinter import *
from users import Users
'''
responsible for the first screen - the login for each user
'''
class login(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.data = Users

    def hush_pass(self):
        # hush password
        pass

    def check_in_sql(self):
        # if user exists in database and password and username match
        # then return true else return false

        try:
            # check if username and password in data base
            Users.check_user_and_pass(self.username, self.password)
            print(f"{self.username} logged in successfully")
            return True

        except:
            print(f"{self.username} failed login attempt ")
            return False


def send_user(userEntry, passEntry):
    # check if password and username are valid
    global logged
    if not logged:
        # check if user is exist
        print(f"sending {userEntry} for a login attempt")
        user = login(userEntry, passEntry)
        logged = user.check_in_sql()
    else:
        print("user already logged")


if __name__ == '__main__':

    tk.mainloop()