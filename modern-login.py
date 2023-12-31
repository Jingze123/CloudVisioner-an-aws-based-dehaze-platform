# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

import icons_rc  # pylint: disable=unused-import
from customized import PasswordEdit
import json
import requests
from upload import UploadForm

class LoginForm(QtWidgets.QWidget):
    """Basic login form.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
 
    def setup_ui(self):
        """Setup the login form.
        """
        self.resize(480, 825)
        self.setWindowTitle("Sign in & Register")
        self.move(300, 100)  # 移动窗口到屏幕上的(300, 100)位置

        self.setStyleSheet(
            """
            QPushButton {
                border-style: outset;
                border-radius: 0px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #cf7500;
                border-style: inset;
            }
            QPushButton:pressed {
                background-color: #ffa126;
                border-style: inset;
            }
            """
        )

        




        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()

        self.widget = QtWidgets.QWidget(self)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget.setStyleSheet(".QWidget{background-color: rgb(20, 20, 40);}")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(9, 0, 0, 0)

        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(35, 25))
        self.pushButton_3.setMaximumSize(QtCore.QSize(35, 25))
        self.pushButton_3.setStyleSheet("color: white;\n"
                                        "font: 13pt \"Verdana\";\n"
                                        "border-radius: 1px;\n"
                                        "opacity: 200;\n")
        self.pushButton_3.clicked.connect(self.close)
        self.verticalLayout_2.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignRight)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 15, -1, -1)

        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(100, 150))
        self.label.setMaximumSize(QtCore.QSize(150, 150))
        self.label.setStyleSheet("image: url(:/icons/icons/rocket_48x48.png);")
        self.verticalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)

        # “CloudVisioner”
        self.cloudVisionerLabel = QtWidgets.QLabel("CloudVisioner", self.widget)
        self.cloudVisionerLabel.setStyleSheet("color: orange; font: 40pt 'Verdana';")
        self.verticalLayout_3.addWidget(self.cloudVisionerLabel, 0, QtCore.Qt.AlignHCenter)



        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setContentsMargins(50, 35, 59, -1)

        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setStyleSheet("color: rgb(231, 231, 231);\n"
                                   "font: 15pt \"Verdana\";")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)

        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit.setStyleSheet("QLineEdit {\n"
                                    "color: rgb(231, 231, 231);\n"
                                    "font: 15pt \"Verdana\";\n"
                                    "border: None;\n"
                                    "border-bottom-color: white;\n"
                                    "border-radius: 10px;\n"
                                    "padding: 0 8px;\n"
                                    "background: rgb(20, 20, 40);\n"
                                    "selection-background-color: darkgray;\n"
                                    "}")
        self.lineEdit.setFocus(True)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)

        self.label_4 = QtWidgets.QLabel(self.widget)
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)

        self.label_3 = QtWidgets.QLabel(self.widget)
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)

        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_3.setStyleSheet("QLineEdit {\n"
                                      "color: rgb(231, 231, 231);\n"
                                      "font: 15pt \"Verdana\";\n"
                                      "border: None;\n"
                                      "border-bottom-color: white;\n"
                                      "border-radius: 10px;\n"
                                      "padding: 0 8px;\n"
                                      "background: rgb(20, 20, 40);\n"
                                      "selection-background-color: darkgray;\n"
                                      "}")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)

        self.lineEdit_2 = PasswordEdit(self.widget)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_2.setStyleSheet("QLineEdit {\n"
                                      "color: rgb(231, 231, 231);\n"
                                      "font: 15pt \"Verdana\";\n"
                                      "border: None;\n"
                                      "border-bottom-color: white;\n"
                                      "border-radius: 10px;\n"
                                      "padding: 0 8px;\n"
                                      "background: rgb(20, 20, 40);\n"
                                      "selection-background-color: darkgray;\n"
                                      "}")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

        self.line = QtWidgets.QFrame(self.widget)
        self.line.setStyleSheet("border: 2px solid white;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.line)

        self.line_3 = QtWidgets.QFrame(self.widget)
        self.line_3.setStyleSheet("border: 2px solid white;")
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.line_3)

        self.line_2 = QtWidgets.QFrame(self.widget)
        self.line_2.setStyleSheet("border: 2px solid white;")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.line_2)

        self.pushButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())

        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 60))
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("color: rgb(231, 231, 231);\n"
                                      "font: 17pt \"Verdana\";\n"
                                      "border: 2px solid orange;\n"
                                      "padding: 5px;\n"
                                      "border-radius: 3px;\n"
                                      "opacity: 200;\n"
                                      "")
        self.pushButton.setAutoDefault(True)
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.pushButton)

        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 60))
        self.pushButton_2.setStyleSheet("color: rgb(231, 231, 231);\n"
                                        "font: 17pt \"Verdana\";\n"
                                        "border: 2px solid orange;\n"
                                        "padding: 5px;\n"
                                        "border-radius: 3px;\n"
                                        "opacity: 200;\n"
                                        "")
        self.pushButton_2.setDefault(False)
        self.pushButton_2.setFlat(False)
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.pushButton_2)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_2.setItem(6, QtWidgets.QFormLayout.SpanningRole, spacerItem)
        self.verticalLayout_3.addLayout(self.formLayout_2)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.horizontalLayout_3.addWidget(self.widget)
        self.horizontalLayout_3.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # 连接按钮的点击事件
        self.pushButton.clicked.connect(self.on_login)
        self.pushButton_2.clicked.connect(self.on_register)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_3.setText(_translate("Form", "X"))
        self.label_2.setText(_translate(
            "Form",
            "<html><head/><body><p><img src=\":/icons/icons/user_32x32.png\"/></p></body></html>"))
        self.label_3.setText(_translate(
            "Form",
            "<html><head/><body><p><img src=\":/icons/icons/lock_32x32.png\"/></p></body></html>"))
        self.label_4.setText(_translate(
            "Form",
            "<html><head/><body><p><img src=\":/icons/icons/mail_32x32.png\"/></p></body></html>"))
        self.pushButton.setText(_translate("Form", "Sign In"))
        self.pushButton_2.setText(_translate("Form", "Register"))
    

    def on_login(self):
        username= self.lineEdit.text()
        email = self.lineEdit_3.text()
        password = self.lineEdit_2.text()
        login_data = {"username": username, "email": email, "password": password}
        response=self.send_to_backend(login_data, "login")
        if response.status_code == 200:
            # 尝试从响应中提取 token
            token = response.text 
            if token:
                print("Received token:", token)
                self.upload_form = UploadForm(token)
                self.upload_form.show()
                self.close()
            else:
                print("Token not found in response")
        else:
            print("Login failed", response.status_code, response.text)

    def on_register(self):
        username= self.lineEdit.text()
        email = self.lineEdit_3.text()
        password = self.lineEdit_2.text()
        register_data = {"username": username, "email": email, "password": password}
        self.send_to_backend(register_data, "register")
        

    def send_to_backend(self, data, operation):
        url = f'https://bh10b6ejeg.execute-api.us-east-2.amazonaws.com/prod/{operation}'
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            print(f"{operation.capitalize()} success")
        else:
            print(f"{operation.capitalize()} fail: {response.text}")
        #在此代码中，需要将 <api-id>, <region>, 和 <stage> 替换为API Gateway实际的API ID、区域和阶段。operation 变量应该对应于API端点，比如 login 或 register
        return response
    
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    login_form = LoginForm()
    login_form.show()

    sys.exit(app.exec_())
