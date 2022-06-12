from server.users import Users
import tkinter as tk
"""
handles signup for each user: creates new user in database
"""


class sign(object):
    def __init__(self, creds):
        self.username, self.password, self.email = creds
        print(f"user {self.username} with {self.email} with password {self.password}")
        self.user = Users()

    def create_a_user(self):
        # creates a user from the given username and password
        print(self.username, self.password, self.email)
        success = self.user.insert_user(self.username, self.password, self.email)
        if success == 1:
            print(f"created {self.username} successfully")
        elif success == -1:
            print(f"can't create username because its already exists")


def send_user(user, password, email):
    # send the data that the user entered to database
    print(user, password,email, "first")
    new_user = signup((user, password, email))
    new_user.create_a_user()


if __name__ == '__main__':
    (user, password, email) = ("lihi", "111", "hero@gmail.com")
    send_user(user,password, email)
