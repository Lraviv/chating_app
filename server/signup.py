from users import Users
import tkinter as tk

class signup(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        print(f"user {self.username} with password {self.password}")

    def create_a_user(self):
        # create a user from the given username and password
        print(self.username, self.password)

        table.insert_user(self.username, self.password)
        print(f"created {self.username} successfully")


def graphics():
    # responsible for the graphics of the game
    logged = False  # a global variable - if user is logged in or not
    win = tk.Tk()
    win.geometry('400x150')
    win.title("Login - SLT")
    # username
    usernameLabel = win.Label(win, text="Username").grid(row=0, column=0)
    username = win.StringVar()
    usernameEntry = win.Entry(win, textvariable=username).grid(row=0, column=1)
    # password
    passwordLabel = win.Label(win, text="Password").grid(row=1, column=0)
    password = win.StringVar()
    passwordEntry = win.Entry(win, textvariable=password, show='*').grid(row=1, column=1)
    # login button
    loginButton = win.Button(win, text="Login", command=lambda: send_user(username.get(), password.get())).grid(row=4,
                                                                                                           column=0)
    #
    tk.mainloop()


def send_user(user,password):
    # send user entered to database
    new_user = signup(user,password)
    new_user.create_a_user()



if __name__ == '__main__':
    table = Users()
    graphics()