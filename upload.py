import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

import icons_rc  # pylint: disable=unused-import
import os
import json
import requests
import base64
from job_manager_window import JobManagerWindow

class UploadForm(QtWidgets.QWidget):
    def __init__(self, token, *args, **kwargs): #总结一下，是否使用 *args 和 **kwargs 取决于您希望方法的调用方式有多灵活，以及您打算如何处理额外的参数。如果您只需要特定的参数（比如 token），那么直接声明这些参数就足够了，不必使用 *args 和 **kwargs,*args 和 **kwargs 是用在更通用的情况下，当您事先不知道将会接收哪些或多少参数时。例如，如果您想允许在方法中传入任意数量的额外参数
        super().__init__(*args, **kwargs)
        self.setup_ui() #设置UI
        self.token=token #存储token

    def setup_ui(self):
        self.resize(480, 825)
        self.setWindowTitle("Upload Image")
        self.move(300, 100)  # 移动窗口到屏幕上的(300, 100)位置
        

        self.setStyleSheet("""
            QWidget {
                background-color: rgb(20, 20, 40);
            }
            QPushButton {
                font: 20pt 'Verdana';  
                border-style: outset;
                border-radius: 0px;
                padding: 6px;
                color: rgb(231, 231, 231);
                background-color: rgb(20, 20, 40);
                border: 2px solid orange;
                
            }
            QPushButton:hover {
                background-color: #cf7500;
                border-style: inset;
            }
            QPushButton:pressed {
                background-color: #ffa126;
                border-style: inset;
            }
        """)


        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.uploadButton = QtWidgets.QPushButton("Upload", self)
        self.uploadButton.clicked.connect(self.select_and_upload_image)
        self.verticalLayout.addWidget(self.uploadButton)

        

    def select_and_upload_image(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            self.upload_image(file_name)

    def upload_image(self, file_name):
        with open(file_name, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            #data = {"username": self.username, "image": encoded_image}
            data = {"image": encoded_image, "originaldatafile":os.path.basename(file_name)}
            response=self.send_to_backend(data, "upload")
            if response.status_code == 200:
                self.job_manager_window = JobManagerWindow(self.token)
                self.job_manager_window.show()
                self.close()
                #也可以解析出token
                # 尝试从响应中提取 token
                # token = response.text 
                # if token:
                #     print("Received token:", token)
                #     self.upload_form = UploadForm(token)
                #     self.upload_form.show()
                #     self.close()
                # else:
                #     print("Token not found in response")
            else:
                print("Upload failed", response.status_code, response.text)

    def send_to_backend(self, data, operation):
        url = f'https://bh10b6ejeg.execute-api.us-east-2.amazonaws.com/prod/{operation}'
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {self.token}' 
                   }

        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print(f"{operation.capitalize()} success")
        else:
            print(f"{operation.capitalize()} fail: {response.text}")   
        return response

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    uploadForm = UploadForm("testuser")  # 假设的用户名
    uploadForm.show()
    sys.exit(app.exec_())
