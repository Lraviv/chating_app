'''
this handles the graphics functions
'''
import base64
import functools
import os
import pickle
import sys
import time
from threading import Thread
from PIL import Image

import PyQt5
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication
import socket
from get_ip_addresses import address
from client.graphics import Ui_MainWindow
from client import client_rsa
from client import speech


class comm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.count = 0
        self.cur_user = ""  # current chat user
        self.thisuser = ""  # name of my user
        label1, label2, label3, label4, label5 = PyQt5.QtWidgets.QLabel(self.main_app),\
                                                 PyQt5.QtWidgets.QLabel(self.main_app),\
                                                 PyQt5.QtWidgets.QLabel(self.main_app), \
                                                 PyQt5.QtWidgets.QLabel(self.main_app),\
                                                 PyQt5.QtWidgets.QLabel(self.main_app)

        self.b1, self.b2, self.b3, self.b4, self.b5 = PyQt5.QtWidgets.QPushButton(self.main_app),  \
                        PyQt5.QtWidgets.QPushButton(self.main_app), PyQt5.QtWidgets.QPushButton(self.main_app),\
                        PyQt5.QtWidgets.QPushButton(self.main_app), PyQt5.QtWidgets.QPushButton(self.main_app)

        self.buttonmsg = {}
        self.labels = [label1, label2, label3, label4, label5]  # list of labels
        self.buttons = [self.b1, self.b2, self.b3, self.b4, self.b5]
        for item in self.buttons: item.hide()
        self.msg_list = []  # list of all current msg in [id, msg] format
        self.label_list = []
        self.chat_users = []  # dict of all users user is chatting with
        self.users_label = [self.userid_button, self.userid_button_2, self.userid_button_3, self.userid_button_4
                            , self.userid_button_5]   # all users label (on the right side)
        self.cur_users = []  # all the users that the user is chatting with

        self.timer = QTimer()
        self.speech = speech.Speech()

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
        self.forgot_password_cmd.clicked.connect(lambda: self.change_window(self.password_reset))
        self.logquit_button.clicked.connect(lambda: exit())
        # ----------in sign up page-------------
        self.signlogin_button.clicked.connect(lambda: self.change_window(self.login_page))  # sign in button
        self.signup_button.clicked.connect(self.send_signup)  # signup button

        # ---------in verification _____________
        self.vertify_button.clicked.connect(self.check_vert)
        self.return_cmd.clicked.connect(lambda: self.change_window(self.login_page))

        # ---------in reset-----------------------
        self.resetpass_button.clicked.connect(lambda: self.forgot_password)
        self.resetpass_button_2.clicked.connect(lambda: self.change_window(self.login_page))
        # ---------in main-------------------------
        self.send_button.clicked.connect(self.send_msg)  # send msg button
        self.start_button.clicked.connect(self.start_speech)  # start speech button
        self.search_user_button.clicked.connect(self.add_user)
        self.pushButton.clicked.connect(self.upload_img)    # upload button

        self.userid_button.clicked.connect(lambda: self.update_current(self.userid_button.text()))
        self.userid_button_2.clicked.connect(lambda: self.update_current(self.userid_button_2.text()))
        self.userid_button_3.clicked.connect(lambda: self.update_current(self.userid_button_3.text()))
        self.userid_button_4.clicked.connect(lambda: self.update_current(self.userid_button_4.text()))
        self.userid_button_5.clicked.connect(lambda: self.update_current(self.userid_button_5.text()))
        # messages
        self.b1.clicked.connect(lambda: self.msg_to_sound(self.b1))
        self.b2.clicked.connect(lambda: self.msg_to_sound(self.b2))
        self.b3.clicked.connect(lambda: self.msg_to_sound(self.b3))
        self.b4.clicked.connect(lambda: self.msg_to_sound(self.b4))
        self.b5.clicked.connect(lambda: self.msg_to_sound(self.b5))


    def send_signin(self):
        # send login credentials to check. if valid then open the slt
        try:
            creds = self.loguser_input.text()+"+"+self.logpass_input.text()
            self.thisuser = self.loguser_input.text()
            # check if password is valid
            self.conn.send_data("02", str(creds))  # sending data for check
            time.sleep(2)
            resp = self.conn.get_answer()
            # check if valid
            if resp == "True":
                self.timer.singleShot(1000, lambda: self.name_label.setText(f"hey {self.thisuser}!"))
                self.change_window(self.main_app)
            else:
                # print error msg and go to check buttons again
                print("[CLIENT] login failed")
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
                time.sleep(3)
                success = self.conn.get_answer()
            print(success)
        except Exception as e:
            print("[EXCEPTION] ", e)

        if success == "True":
            print("user proceeding to validation")
            self.change_window(self.vertification)
        else:
            print("sign up failed")
            QTimer.singleShot(1000, lambda: self.warn_label_sign.setText(info))

    def check_vert(self):
        # check if the code that the user clicked is valid
        user_code = self.vertcode_input.text()
        self.conn.send_data("01", user_code)
        time.sleep(2)
        resp = self.conn.get_answer()
        if resp == 'True':
            print("user successfully passed verification")
            self.change_window(self.login)
        else:
            print("user failed verification")
            self.warn_label_vert.setText("code does not match, try again")

    def change_window(self, win):
        # change current displaying window
        self.entry.setCurrentWidget(win)

    def send_msg(self):
        # send msg to another user, and handle it being displayed on screen
        if self.cur_user!="":
            textmsg = self.msg_edit_box.toPlainText()   # get the message from the text box
            data = self.cur_user+"+"+textmsg
            self.msg_edit_box.clear()
            self.display_msg(0,textmsg)  # display msg box
            self.conn.send_data("04", data)     # sending data to current chat user
        else:
            print("user don't have any other users")

    def display_msg(self, user_id, text):
        # handles message display, 0 is user 1 is the other user
        this_msg = [user_id, text]
        self.msg_list.insert(0, this_msg)   # insert message to start of list
        for msg in self.msg_list:   # check if the message is empty
            if len(msg[1]) == 0:
                self.msg_list.remove(msg)

        # check if there are too much messages for screen
        if len(self.msg_list) > 5:
            del self.msg_list[-1]
        print(f"there are {len(self.msg_list)} messages")

        # display all labels onscreen
        count = 0
        for msg in self.msg_list:
            print(f"displaying {msg[1]} from user {msg[0]}")
            if msg[0] == 0:   # this is user's msg
                style = "background-color: rgb(85, 170, 255);\n"
                x, y = 380, (490+(count)*-100)
            else:   # if it's the other user
                style = "background-color: rgb(217, 217, 217);\n"
                x, y = 70, (490+(count)*-100)
            style += 'border-radius: 15px;\n font: 9pt "Arial";'

            self.buttons[count].setGeometry(PyQt5.QtCore.QRect(x-55, y+35, 51, 31))
            self.buttonmsg[self.buttons[count]] = msg[1]
            self.buttons[count].setText("▶")
            self.buttons[count].setStyleSheet('font: 10pt "Arial"')

            self.labels[count].setGeometry(PyQt5.QtCore.QRect(x, y, 421, 91))
            self.labels[count].setWordWrap(True)

            self.labels[count].setStyleSheet(style)
            self.labels[count].setText(" " + str(msg[1]))
            self.labels[count].show()
            self.buttons[count].show()
            count += 1

    def start_speech(self):
        # start recording and convert the audio to text
        text = self.speech.recognize()
        self.msg_edit_box.setPlainText(text)
        self.msg_edit_box.show()

    def msg_to_sound(self, button):
        # if user clicks on msg play this msg
        print(button)
        label = self.buttonmsg.get(button)
        print(f"label is {label} ")
        try:
            if label != '':
                self.speech.speak(label)
        except Exception as e:
            print(f"[SOUND ERROR] {e}")

    def add_user(self):
        # add user to chats
        user = self.search_user_line.text()
        print(f"adding {user}")
        self.conn.send_data("05", str(user))
        time.sleep(1)
        resp = self.conn.get_answer()
        if resp == "True":
            for label in self.users_label:
                if label.text() == '' and label.text() not in self.cur_users:
                    label.setText(str(user))

                    self.cur_users.append(user)
                    self.cur_user = user
                    return

            if self.count == 5:
                self.count = 0

            self.users_label[self.count].setText('')
            self.add_user()
            self.count += 1
        else:
            print("user doesn't exist / not online")

    def update_current(self, username):
        print(f"user is chatting with {username}")
        for label in self.labels: label.hide()  # hide all labels
        for button in self.buttons: button.hide()  # hide all buttons
        self.cur_user = username

    def upload_img(self):
        # handles img uploading
        if self.cur_user == '':
            print("user didn't added users yet")
            return
        # create option to open file
        options = PyQt5.QtWidgets.QFileDialog.Options()
        options |= PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "PNG File (*.png)", options=options)
        if fileName:
            print(fileName)
            self.file = fileName
            data = self.cur_user
            self.conn.send_data("08",data)

            file = open(self.file, "rb")
            img_str = file.read(2048)

            while img_str:
                self.conn.send_data("07",str(img_str))
                img_str = file.read(2048)
            file.close()
            self.conn.send_data("07", "א")

    def forgot_password(self):
        #  handle click on ''
        self.change_window(self.password_reset)
        if self.pass_input2.find("+") <=0 and len(self.pass_input2) < 8:
            creds = self.pass_input + "+" + self.pass_input2
            self.conn.send_data("09", creds)    # request to be sent a code
            self.change_window(self.vertification)
            self.conn.send_data("10", self.vertcode_input)
            time.sleep(2)
            if self.conn.get_answer() == 'True':
                print("password updated successfully")
                self.change_window(self.login_page)
            else:
                print("couldn't update password")
        else:
            print("password is invalid")



# ----------------------------------------------------------------------------------------------------------------------


class connect():
    def __init__(self):
        add = address()
        self.host = add.get_server_ip()
        self.port = add.get_port()
        self.buffer_size = 1024
        self.image_mode = False
        print(f'connecting to {self.host} with port {self.port}')
        self.response = ""
        self.public_key = ""

    def send_data(self, id, data):
        # sending msg in format
        #self.encoding_data(data)
        self.data = self.encrypt(id, data)  # encrypting data
        print("sending: ", self.data)
        self.ClientSocket.send(str.encode(self.data))

    def get_answer(self):
        # receiving answer from server
        return self.response

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
        # receiving loop from server:
        while True:
            if not self.image_mode:
                response = self.ClientSocket.recv(1024)
                response = response.decode('utf-8')
                print("[SERVER] "+response)
                if response != None or response != '':
                    if response == "True" or response == "False":
                        self.response = response
                    else:
                        self.commit_action(response)
                else:
                    print("response is None")
            else:
                print("starting to get image")
                img = open("image.png", 'wb')
                recv_data = self.ClientSocket.recv(2048)
                while recv_data:
                    img.write(recv_data)
                    recv_data = self.ClientSocket.recv(2048)
                img.close()
                print("here")
                if recv_data == 'א':
                    self.image_mode = False
                win.display_msg(1, "image.png")
                print("image mode done")




    def encrypt(self, id, data):
        # get msg in format  id|size|data before sending
        size = len(data.encode())
        new_data = (id + "|" + str(size) + "|" + str(data))
        return new_data

    def commit_action(self, rep):
        # sort which action to do
        all_data = rep.split("|")
        if all_data[0] == "00":  # receive and display message
            data = all_data[1].split("+")   # origin+msg_data
            win.display_msg(1, data[1])

        elif all_data[0] == "01":  # get key
            self.public_key = all_data[1]
            print(f"public key is {self.public_key}")

        elif all_data[0] == "02":     # receive image
            data = all_data[1].split("+")   # origin + image
            print(f"image is {data[1]}")
            win.display_msg(1, "image")
            self.buffer_size = 1024

        elif all_data[0] == "03":     # get image size
            self.image_mode = True
            self.origin = all_data[1]
            print(f"image incoming from {all_data[1]}")

        else:
            print("not in commit")

    def generate_priv(self):
        pass

    def encoding_data(self, data):
        try:
            msg = client_rsa.encode(data, self.public_key)
            print("encoded msg" + str(msg))
            return msg
        except:
            print("can't encode")
            return data

    def close_con(self):
        self.ClientSocket.close()


if __name__ == "__main__":
    global win
    app = QApplication(sys.argv)
    win = comm()
    win.show()

    sys.exit(app.exec_())

