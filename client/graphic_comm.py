'''
this handles the graphics functions
'''
import sys
import threading

import PyQt5
from PyQt5.QtWidgets import QMainWindow,QApplication
import asyncio
from client import window2
from graphics import Ui_MainWindow
from login import Login, Sign
import waiting

global turn
turn = False

class comm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.validation = False
        self.check_buttons()


    def check_buttons(self):
        # Check if button has been pressed and execute its function
        self.retranslateUi(self)
        # ---------in opening page-------------
        self.open_button.clicked.connect(lambda: self.change_window(self.login_page))

        # ----------in login page-----------
        self.login_button.clicked.connect(self.send_signin)  # login button
        self.logsign_button.clicked.connect(lambda: self.change_window(self.signup_page))  # signup button
        self.forgot_password_cmd.clicked.connect(lambda: self.change_window(self.vertification))
        self.logquit_button.clicked.connect(lambda: exit())
        # ----------in sign up page-------------
        self.signlogin_button.clicked.connect(lambda: self.change_window(self.login_page))  # signin button
        self.signup_button.clicked.connect(self.send_signup)  # signup button

        # ---------in verification _____________
        self.vertify_button.clicked.connect(self.check_vert)
        self.return_cmd.clicked.connect(lambda: self.change_window(self.login_page))

        # ---------in main ______________________ buttons: reset,



    def send_signin(self):
        # send login credentials to check. if valid try then open the slt
        try:
            global turn
            print("login try...")
            creds = (self.loguser_input.text(), self.logpass_input.text())
            print(creds)
            self.user = Login(creds)
            self.validation = self.user.is_valid()  # get true if login attempt succeed

            if self.validation:
                turn = True
                print("login succeeded")

                print("destroyed", turn)
                self.destroy()

            else:
                # print error msg and go to check buttons again
                print("login failed")
                info = "login failed, try again..."
                self.label = PyQt5.QtWidgets.QLabel(info)
                self.label.move(self.warn_label_log.width(),self.warn_label_log.height())
                self.label.setStyleSheet("border: 1px solid black;")
                self.label.show()
                #self.warn_label_sign.setText()
                self.check_buttons()

        except Exception as e:
            print("[ERROR] ", e)

    def send_signup(self):
        ''' add creds from client to database, if signup is successful then
        continue to main screen '''
        creds = (self.signuser_input.text(), self.signpass_input.text(), self.signemail_input.text())
        self.user = Sign(creds)
        success = self.user.add_to_db()
        if success:
            print("user had been added to database")
            self.change_window(self.login_page)
            self.frame()
        else:
            print("sign up failed")
            pass

    def check_vert(self):
        # check if the code that the user clicked is valid
        user_code = self.vertcode_input.text()
        # here send code to server @TODO


    def change_window(self, win):
        # change current displaying window
        self.entry.setCurrentWidget(win)
        self.check_buttons()

def check(turn):
    # get validation
    while True:
        if turn:
            turn = False
            print("exiting")
            window2.start()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = comm()
    win.show()

    t = threading.Thread(target=check, args=(turn,))
    t.start()
    t.join()

    sys.exit(app.exec())

