# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'project.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(858, 544)
        self.windows = QtWidgets.QWidget(MainWindow)
        self.windows.setObjectName("windows")
        self.slt_window = QtWidgets.QStackedWidget(self.windows)
        self.slt_window.setGeometry(QtCore.QRect(-20, 0, 901, 571))
        self.slt_window.setObjectName("slt_window")
        self.login_page = QtWidgets.QWidget()
        self.login_page.setObjectName("login_page")
        #self.slt_bg = QtGui.QPixmap('bg_slt.jpg')

        self.user_input = QtWidgets.QLineEdit(self.login_page)
        self.user_input.setGeometry(QtCore.QRect(260, 190, 321, 61))
        palette = QtGui.QPalette()
        self.user_input.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setStrikeOut(False)
        self.user_input.setFont(font)
        self.user_input.setStyleSheet("QLineEdit { \n"
"    border: 2px solid rgb(37,39,48);\n"
"    border-radius: 20px;\n"
"    padding-left: 20px;\n"
"    padding-right: 20px;\n"
"}\n"
"QLineEditor:hover{\n"
"    border: 2px solid rgb(48,50,62);\n"
"}\n"
"QLineEdit:focus{\n"
"    border: 2px solid rgb(85,179,255);\n"
"}")
        self.user_input.setText("")
        self.user_input.setObjectName("user_input")
        self.pass_input = QtWidgets.QLineEdit(self.login_page)
        self.pass_input.setGeometry(QtCore.QRect(260, 270, 321, 61))
        palette = QtGui.QPalette()
        self.pass_input.setPalette(palette)
        font = QtGui.QFont()
        """
        
        obj_line = ""
        obj_line.connect(enter,->check_pass)
        checkpass:
            obj_line.gettext()       
        """
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setStrikeOut(False)
        self.pass_input.setFont(font)
        self.pass_input.setStyleSheet("QLineEdit { \n"
"    border: 2px solid rgb(37,39,48);\n"
"    border-radius: 20px;\n"
"    \n"
"    padding-left: 20px;\n"
"    padding-right: 20px;\n"
"}\n"
"QLineEditor:hover{\n"
"    border: 2px solid rgb(48,50,62);\n"
"}\n"
"QLineEdit:focus{\n"
"    border: 2px solid rgb(85,179,255);\n"
"}")
        self.pass_input.setText("")
        self.pass_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_input.setCursorPosition(0)
        self.pass_input.setObjectName("pass_input")
        self.pushButton = QtWidgets.QPushButton(self.login_page)
        self.pushButton.setGeometry(QtCore.QRect(350, 350, 131, 51))
        self.pushButton.setStyleSheet("QPushButton{\n"
"    font: 20pt \"MS Shell Dlg 2\";\n"
"    border: 2px solid rgb(37,39,48);\n"
"    border-radius: 20px\n"
"}\n"
"QPushButton:hover{\n"
"    color: rgb(85, 170, 255);\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.signup_cmd = QtWidgets.QCommandLinkButton(self.login_page)
        self.signup_cmd.setGeometry(QtCore.QRect(490, 360, 222, 48))
        self.signup_cmd.setObjectName("signup_cmd")
        self.bg_pic_2 = QtWidgets.QLabel(self.login_page)
        self.bg_pic_2.setGeometry(QtCore.QRect(-20, -160, 1221, 827))
        self.bg_pic_2.setMinimumSize(QtCore.QSize(1221, 821))
        self.bg_pic_2.setObjectName("bg_pic_2")
        self.header_label_2 = QtWidgets.QLabel(self.login_page)
        self.header_label_2.setGeometry(QtCore.QRect(190, 90, 491, 71))
        self.header_label_2.setStyleSheet("font: 20pt \"OCR A Extended\";")
        self.header_label_2.setObjectName("header_label_2")
        self.bg_pic_2.raise_()
        self.user_input.raise_()
        self.pass_input.raise_()
        self.pushButton.raise_()
        self.signup_cmd.raise_()
        self.header_label_2.raise_()
        self.slt_window.addWidget(self.login_page)
        self.signup_page = QtWidgets.QWidget()
        self.signup_page.setObjectName("signup_page")
        self.pass_input_2 = QtWidgets.QLineEdit(self.signup_page)
        self.pass_input_2.setGeometry(QtCore.QRect(270, 250, 321, 61))
        palette = QtGui.QPalette()
        self.pass_input_2.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setStrikeOut(False)
        self.pass_input_2.setFont(font)
        self.pass_input_2.setStyleSheet("QLineEdit { \n"
"    border: 2px solid rgb(37,39,48);\n"
"    border-radius: 20px;\n"
"    \n"
"    padding-left: 20px;\n"
"    padding-right: 20px;\n"
"}\n"
"QLineEditor:hover{\n"
"    border: 2px solid rgb(48,50,62);\n"
"}\n"
"QLineEdit:focus{\n"
"    border: 2px solid rgb(85,179,255);\n"
"}")
        self.pass_input_2.setText("")
        self.pass_input_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_input_2.setCursorPosition(0)
        self.pass_input_2.setObjectName("pass_input_2")
        self.user_input_2 = QtWidgets.QLineEdit(self.signup_page)
        self.user_input_2.setGeometry(QtCore.QRect(270, 170, 321, 61))
        palette = QtGui.QPalette()
        self.user_input_2.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setStrikeOut(False)
        self.user_input_2.setFont(font)
        self.user_input_2.setStyleSheet("QLineEdit { \n"
"    border: 2px solid rgb(37,39,48);\n"
"    border-radius: 20px;\n"
"    padding-left: 20px;\n"
"    padding-right: 20px;\n"
"}\n"
"QLineEditor:hover{\n"
"    border: 2px solid rgb(48,50,62);\n"
"}\n"
"QLineEdit:focus{\n"
"    border: 2px solid rgb(85,179,255);\n"
"}")
        self.user_input_2.setText("")
        self.user_input_2.setObjectName("user_input_2")
        self.signup_button = QtWidgets.QPushButton(self.signup_page)
        self.signup_button.setGeometry(QtCore.QRect(360, 350, 131, 51))
        self.signup_button.setStyleSheet("QPushButton{\n"
"    font: 20pt \"MS Shell Dlg 2\";\n"
"    border: 2px solid rgb(37,39,48);\n"
"    border-radius: 20px\n"
"}\n"
"QPushButton:hover{\n"
"    color: rgb(85, 170, 255);\n"
"}")
        self.signup_button.setObjectName("signup_button")
        self.bg_pic = QtWidgets.QLabel(self.signup_page)
        #self.pixmap = QtGui.QPixmap('bg_slt.jpg')
        #self.bg_pic.setPixmap(self.pixmap)
        self.bg_pic.setGeometry(QtCore.QRect(-20, -170, 1221, 827))
        self.bg_pic.setMinimumSize(QtCore.QSize(1221, 821))
        self.bg_pic.setObjectName("bg_pic")
        self.header_label = QtWidgets.QLabel(self.signup_page)
        self.header_label.setGeometry(QtCore.QRect(200, 80, 491, 71))
        self.header_label.setStyleSheet("font: 20pt \"OCR A Extended\";")
        self.header_label.setObjectName("header_label")
        self.signin_cmd = QtWidgets.QCommandLinkButton(self.signup_page)
        self.signin_cmd.setGeometry(QtCore.QRect(490, 360, 111, 41))
        self.signin_cmd.setObjectName("signin_cmd")
        self.bg_pic.raise_()
        self.pass_input_2.raise_()
        self.user_input_2.raise_()
        self.signup_button.raise_()
        self.header_label.raise_()
        self.signin_cmd.raise_()
        self.slt_window.addWidget(self.signup_page)
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.slt_window.addWidget(self.page)
        MainWindow.setCentralWidget(self.windows)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 858, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.user_input.setPlaceholderText(_translate("MainWindow", "Username"))
        self.pass_input.setPlaceholderText(_translate("MainWindow", "Password"))
        self.pushButton.setText(_translate("MainWindow", "login"))
        self.signup_cmd.setText(_translate("MainWindow", "sign up"))
        self.bg_pic_2.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/images/bg_slt.jpg\"/></p></body></html>"))
        self.header_label_2.setText(_translate("MainWindow", "Sign Language Translator"))
        self.pass_input_2.setPlaceholderText(_translate("MainWindow", "Password"))
        self.user_input_2.setPlaceholderText(_translate("MainWindow", "Username"))
        self.signup_button.setText(_translate("MainWindow", "signup"))
        self.bg_pic.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/images/bg_slt.jpg\"/></p></body></html>"))
        self.header_label.setText(_translate("MainWindow", "Sign Language Translator"))
        self.signin_cmd.setText(_translate("MainWindow", "sign in "))

import wall


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())