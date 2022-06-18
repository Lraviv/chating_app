'''
this handles the graphics functions
'''
import sys
import PyQt5
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore
import socket
#import client.window2
from client.graphics import Ui_MainWindow
from login import Login, Sign
from threading import Thread


class comm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.my_msg_label.hide()
        self.others_msg_label.hide()

        self.msg_list = []  # list of all current msg in [id, msg] format
        self.label_list = []
        self.chat_users = [] # dict of all users user is chatting with
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

        # ---------in reset-----------------------

        #---------in main-------------------------
        self.send_button.clicked.connect(self.send_msg)  # send msg button
        self.start_button.clicked.connect(self.start_speech)  # start speech button


    def send_signin(self):
        # send login credentials to check. if valid try then open the slt
        global c
        try:
            creds = self.loguser_input.text()+"+"+self.logpass_input.text()
            # check if password is valid
            print("login try: ", creds)
            resp = c.send_data("02", str(creds)) # sending data for check   #@TODO solve the bug
            # check if valid
            if resp == "True":
                print("login succeeded")
                self.change_window(self.main_app)
                self.check_buttons()
            else:
                # print error msg and go to check buttons again
                print("login failed")
                info = "login failed, try again..."
                QTimer.singleShot(3 * 1000, lambda: self.warn_label_log.setText(info))
                self.check_buttons()

        except Exception as e:
            print("[ERROR] ", e)


    def send_signup(self):
        ''' add creds from client to database, if signup is successful then
        continue to main screen '''
        global c
        creds = self.signuser_input.text()+"+"+self.signpass_input.text()+"+"+self.signemail_input.text()
        # check if password is valid
        print(str(creds))
        success = False
        try:
            if len(self.signpass_input.text()) < 8:
                info = "password is too short"
                print(info)
                success = False
            else:
                print('trying')
                info = "sign up failed"
                success = c.send_data("03", str(creds))
            print(success)
        except Exception as e:
            print("[EXCEPTION] ", e)

        if success == "True":
            print("user had been added to database")
            self.change_window(self.login_page)
            self.check_buttons()
        else:
            print("sign up failed")
            QTimer.singleShot(3 * 1000, lambda: self.warn_label_sign.setText(info))
            self.check_buttons()


    def check_vert(self):
        # check if the code that the user clicked is valid
        user_code = self.vertcode_input.text()
        # here send code to server @TODO


    def change_window(self, win):
        # change current displaying window
        self.entry.setCurrentWidget(win)


    def send_msg(self):
        # send msg to another user
        # handle user's edit msg box
        textmsg = self.msg_edit_box.toPlainText()  #@TODO this is the msg client wants to send
        print(textmsg)
        self.msg_edit_box.clear()
        # display msg box
        self.display_msg(0, textmsg)

    def display_msg(self, id, text):
        # handles message display, 0 is user 1 is other
        this_msg = [id, text]
        self.msg_list.insert(0, this_msg)   # insert message to start of list
        # check if there are too much messages for screen
        if len(self.msg_list) > 5:
            print(f"there are {len(self.msg_list)} messages")
            del self.msg_list[-1]
            print(f"popped - now theres {len(self.msg_list)}")
        else:
            print(f"there are {len(self.msg_list)} messages")

        for label in self.label_list:
            label.clear()
        print(self.msg_list)
        # display all labels onscreen
        for msg in self.msg_list:
            print(f"displaying {msg[1]} from user {msg[0]}")
            label = PyQt5.QtWidgets.QLabel(self.main_app)
            if msg[0] == 0:   # this is user's msg
                style = "background-color: rgb(85, 170, 255);\n"
                x, y = 380, (490+(len(self.msg_list)-1)*-100)
            else:   # if it's the other user
                style = "background-color: rgb(85, 170, 255);\n"
                x, y = 70, (490+(len(self.msg_list)-1)*-100)

            style += 'border-radius: 15px;\n font: 9pt "Arial";'
            label.setGeometry(PyQt5.QtCore.QRect(x, y, 421, 91))
            QTimer.singleShot(3 * 1000, lambda: label.setStyleSheet(style))
            QTimer.singleShot(3 * 1000, lambda: label.setText(" " + str(msg[1])))
            label.show()
            #QTimer.singleShot(3 * 1000, lambda: label.show())
            self.label_list.append(label)

    def start_speech(self):
        # start recording
        #text = client.window2.recognize()
        #print(text)
        #self.msg_edit_box.setPlainText(text)
        #self.msg_edit_box.show()
        pass

class connect():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8448
        self.data = ''

    def send_data(self, id, data):
        # sending msg in format
        self.data = self.encrypt(id, data)  # encrypting data
        print("sending: ", self.data)
        self.ClientSocket.send(str.encode(self.data))

        # receiving answer from server
        Response = self.ClientSocket.recv(1024)  # receive from server
        rep = Response.decode('utf-8')
        print("[SERVER]: ", rep)
        # decrypt
        #self.decrypt(rep)
        return rep

    def receive(self):
        self.ClientSocket = socket.socket()
        # establish connection
        print('Waiting for connection')
        try:
            self.ClientSocket.connect((self.host, self.port))
            print("connected to server")
        except socket.error as e:
            print(str(e))

    def encrypt(self, id, data):
        # get msg in format  id|size|data before sending
        size = len(data.encode())
        new_data = (id + "|" + str(size) + "|" + str(data))
        return new_data

    def decrypt(self, data):
        # first encrypt msg then commit action
        new_data = data.split("|")
        id, data = new_data[0], new_data[2]
        #self.commit_action(id,data)

    def close_con(self):
        self.ClientSocket.close()

if __name__ == "__main__":
    global c
    app = QApplication(sys.argv)
    win = comm()
    c = connect()
    gui_thread = Thread(target=win.show())
    net_thread = Thread(target=c.receive)

    gui_thread.start()
    net_thread.start()

    net_thread.join()
    gui_thread.join()

    c.close_con()
    sys.exit(app.exec_())

