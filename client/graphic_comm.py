'''
this handles the graphics functions
'''
import sys
import time

import PyQt5
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication
import socket
from get_ip_addresses import address
from client.graphics import Ui_MainWindow
from threading import Thread


class comm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.count = 0
        self.cur_user = ""  # current chat user
        self.thisuser = ""  # name of my user

        self.msg_list = []  # list of all current msg in [id, msg] format
        self.label_list = []
        self.chat_users = []  # dict of all users user is chatting with
        self.users_label = [self.userid_button, self.userid_button_2, self.userid_button_3, self.userid_button_4
                            , self.userid_button_5]   # all users label (on the right side)
        self.cur_users = []  # all the users that the user is chatting with

        self.timer = QTimer()

        self.conn = connect()
        net_thread = Thread(target=self.conn.receive_loop)
        net_thread.start()

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
        self.signlogin_button.clicked.connect(lambda: self.change_window(self.login_page))  # sign in button
        self.signup_button.clicked.connect(self.send_signup)  # signup button

        # ---------in verification _____________
        self.vertify_button.clicked.connect(self.check_vert)
        self.return_cmd.clicked.connect(lambda: self.change_window(self.login_page))

        # ---------in reset-----------------------

        #---------in main-------------------------
        self.send_button.clicked.connect(self.send_msg)  # send msg button
        self.start_button.clicked.connect(self.start_speech)  # start speech button
        self.search_user_button.clicked.connect(self.add_user)
        self.userid_button.clicked.connect(lambda: self.update_current(self.userid_button.text()))
        self.userid_button_2.clicked.connect(lambda: self.update_current(self.userid_button_2.text()))
        self.userid_button_3.clicked.connect(lambda: self.update_current(self.userid_button_3.text()))
        self.userid_button_4.clicked.connect(lambda: self.update_current(self.userid_button_4.text()))
        self.userid_button_5.clicked.connect(lambda: self.update_current(self.userid_button_5.text()))

    def send_signin(self):
        # send login credentials to check. if valid try then open the slt
        try:
            creds = self.loguser_input.text()+"+"+self.logpass_input.text()
            self.thisuser = self.loguser_input.text()
            # check if password is valid
            print("login try: ", creds)
            self.conn.send_data("02", str(creds))  # sending data for check
            time.sleep(3)
            resp = self.conn.get_answer()
            print("response is "+resp)
            # check if valid
            if resp == "True":
                print("login succeeded")
                self.change_window(self.main_app)
            else:
                # print error msg and go to check buttons again
                print("login failed")
                info = "login failed, try again..."
                self.timer.singleShot(1000, lambda: self.warn_label_log.setText(info))

        except Exception as e:
            print("[ERROR] ", e)


    def send_signup(self):
        ''' add creds from client to database, if signup is successful then
        continue to main screen '''
        creds = self.signuser_input.text()+"+"+self.signpass_input.text()+"+"+self.signemail_input.text()
        # check if password is valid
        print(str(creds))
        success = "False"
        try:
            if len(self.signpass_input.text()) < 8 or self.signpass_input.text().find("+")>0:
                info = "password is invalid"
                print(info)
            else:
                print('trying to sign up...')
                info = "sign up failed"
                self.conn.send_data("03", str(creds))  # send that sign up failed
                success = self.conn.get_answer()
            print(success)
        except Exception as e:
            print("[EXCEPTION] ", e)

        if success == "True":
            print("user had been added to database")
            self.change_window(self.login_page)
        else:
            print("sign up failed")
            #QTimer.singleShot(3 * 1000, lambda: self.warn_label_sign.setText(info))

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
        if self.cur_user!="":
            textmsg = self.msg_edit_box.toPlainText()
            data = self.cur_user+"+"+textmsg
            self.msg_edit_box.clear()
            self.display_msg(0,textmsg) # display msg box
            self.conn.send_data("04", data)     # sending data to current chat user
        else:
            print("user don't have any other users")

    def display_msg(self, user_id, text):
        # handles message display, 0 is user 1 is other
        this_msg = [user_id, text]
        self.msg_list.insert(0, this_msg)   # insert message to start of list
        for msg in self.msg_list:
            if len(msg[1]) == 0:
                self.msg_list.remove(msg)

        # check if there are too much messages for screen
        if len(self.msg_list) > 5:
            print(f"there are {len(self.msg_list)} messages")
            del self.msg_list[-1]
            print(f"popped - now theres {len(self.msg_list)}")
        else:
            print(f"there are {len(self.msg_list)} messages")

        for label in self.label_list:
            label.clear()
            self.label_list.remove(label)
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
            label.setWordWrap(True)
            self.label_list.append(label)
            self.timer.singleShot(1000, lambda: label.setStyleSheet(style))
            self.timer.singleShot(1000, lambda: label.setText(" " + str(msg[1])))
            self.timer.singleShot(1000, lambda: label.show())


    def start_speech(self):
        # start recording
        #text = speech.recognize()
        #print(text)
        #self.msg_edit_box.setPlainText(text)
        #self.msg_edit_box.show()
        pass

    def add_user(self):
        # add user to chats
        user = self.search_user_line.text()
        print(f"adding {user}")
        self.conn.send_data("05", str(user))
        resp = self.conn.get_answer()
        if resp == "True":
            QTimer.singleShot(1000, lambda: self.userid_button.setText(str(user)))
            self.cur_users.append(user)
            self.cur_user = user
        else:
            print("user doesn't exist / not online")

    def update_current(self, username):
        print(f"user is chatting with {username}")
        self.cur_user = username

# ----------------------------------------------------------------------------------------------------------------------


class connect():
    def __init__(self):
        add = address()
        self.host = add.get_server_ip()
        self.port = add.get_port()
        print(f'connecting to {self.host} with port {self.port}')
        self.response = ""

    def send_data(self, id, data):
        # sending msg in format
        self.data = self.encrypt(id, data)  # encrypting data
        print("sending: ", self.data)
        self.ClientSocket.send(str.encode(self.data))

    def get_answer(self):
        return self.response
        # receiving answer from server
        #Response = self.ClientSocket.recv(1024)  # receive from server
        #rep = Response.decode('utf-8')
        #print("[SERVER] ", rep)
        # decrypt
        #self.decrypt(rep)
        #return rep

    def receive_loop(self):
        global win
        self.ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # establish connection
        print('Waiting for connection')
        try:
            self.ClientSocket.connect((self.host, self.port))
            print(f"connected to server as {self.ClientSocket}")
        except socket.error as e:
            print(str(e))

        while True:
            response = self.ClientSocket.recv(1024)
            response = response.decode('utf-8')
            print("[SERVER] "+response)
            if response != None:
                if response == "True" or response == "False":
                    print("in true/false")
                    self.response = response
                else:
                    self.commit_action(response)


    def encrypt(self, id, data):
        # get msg in format  id|size|data before sending
        size = len(data.encode())
        new_data = (id + "|" + str(size) + "|" + str(data))
        return new_data

    def commit_action(self, rep):
        # sort which action to do
        print("in commit")
        try:
            data = rep.split("+")   # -qs+origin+msg_data
            win.display_msg(1, data[2])
        except:
            print("can't display")

    def close_con(self):
        self.ClientSocket.close()


if __name__ == "__main__":
    global win
    app = QApplication(sys.argv)
    win = comm()
    win.show()

    sys.exit(app.exec_())

