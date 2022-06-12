'''
this handles the graphics functions
'''
import sys
import PyQt5
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



    def send_signin(self):
        # send login credentials to check. if valid try then open the slt
        try:
            global c
            print("login try...")
            creds = self.loguser_input.text()+"+"+self.logpass_input.text()
            print(creds)
            #self.user = Login(creds)

            rep = c.send_data(str(creds))


            #self.validation = self.user.is_valid()  # get true if login attempt succeed
            # check if valid
            if rep:
                self.change_window(self.main_app)
                print("login succeeded")
                self.chat()

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


    def chat(self):
        # handles main functions
        self.send_button.clicked.connect(self.send_msg)  # send msg button
        self.start_button.clicked.connect(self.start_speech)  # start speech button

        self.check_buttons()


    def send_msg(self):
        # send msg to another user
        # handle user's edit msg box

        self.my_msg_label.show()
        textmsg = self.msg_edit_box.toPlainText()  #@TODO this is the msg client wants to send
        print(textmsg)
        self.msg_edit_box.clear()

        self.my_msg_label.setText(str(textmsg))

        for x in range(0,10):
            QtCore.QCoreApplication.processEvents()

        self.my_msg_label.show()



        # display msg box
        #self.display_msg(0, textmsg)

    def display_msg(self, id, text):
        # handles message display, 0 is user 1 is other
        this_msg = [id, text]
        self.msg_list += this_msg
        # convert msg to label
        this_label = self.turn_to_label(this_msg)
        self.label_list += this_label
        # check if there are too much messages for screen
        if len(self.msg_list) >5:
            self.msg_list.pop()
            self.label_list.pop()
        # display all labels onscreen
        for label in self.label_list:
            print(label)

    def turn_to_label(self, msg):
        # turn msg format to label
        label = PyQt5.QtWidgets.QLabel(self.main_app)
        # if it's user's msg the background is blue
        if msg[0] == 0:
            label.setStyleSheet("background-color: rgb(85, 170, 255);\n")
            x,y = 380, 490  # user tab + initial height
        # if it's other user the background is grey
        else:
            label.setStyleSheet("background-color: rgb(85, 170, 255);\n")
            x,y = 70, 490

        label.setGeometry(PyQt5.QtCore.QRect(x, y, 421, 91))
        label.setStyleSheet("border-radius: 15px;\n"
                            "font: 9pt \"Arial\";")

        label.setText(msg[1])
        return label

    def start_speech(self):
        # start recording
        #text = client.window2.recognize()
        #print(text)
        #self.msg_edit_box.setPlainText(text)
        #self.msg_edit_box.show()
        self.chat()

class connect():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8448
        self.data = ''

    def send_data(self, data):
        self.data = data
        print("sending: ", self.data)
        self.ClientSocket.send(str.encode(self.data))
        Response = self.ClientSocket.recv(1024)  # receive from server
        rep = Response.decode('utf-8')
        print(rep)
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

        Response = self.ClientSocket.recv(1024)
        while True:
            # receive loop
            Response = self.ClientSocket.recv(1024)  # receive from server
            print(Response.decode('utf-8'))

        ClientSocket.close()


if __name__ == "__main__":
    global c
    app = QApplication(sys.argv)
    win = comm()
    c = connect()
    gui_thread = Thread(target=win.show())
    net_thread = Thread(target=c.receive)

    gui_thread.start()
    net_thread.start()

    #win.show()
    sys.exit(app.exec_())

