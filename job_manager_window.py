import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

import icons_rc  # pylint: disable=unused-import
import os
import json
import requests
import base64

class JobManagerWindow(QtWidgets.QWidget):
    def __init__(self, token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
        self.token=token

    def setup_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.resize(480, 825)
        self.setWindowTitle("Job List")
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


        # 按钮：获取任务列表
        self.get_jobs_button = QtWidgets.QPushButton("Get Job List")
        self.get_jobs_button.clicked.connect(self.get_job_list)
        self.layout.addWidget(self.get_jobs_button)

        # 显示任务列表
        self.jobs_list_widget = QtWidgets.QListWidget()
        self.layout.addWidget(self.jobs_list_widget)

        # 输入框和按钮：下载任务结果
        self.download_layout = QtWidgets.QHBoxLayout()
        self.job_id_input = QtWidgets.QLineEdit()
        self.job_id_input.setMinimumSize(200, 40)  # 设置最小尺寸
        self.job_id_input.setStyleSheet("""
            QLineEdit {
                font: 16pt 'Verdana';  
                border: 1px solid gray; 
                border-radius: 5px;  
                padding: 5px; 
            }
        """)

        self.download_button = QtWidgets.QPushButton("Download Job Result")
        self.download_button.clicked.connect(self.download_job_result)
        self.download_layout.addWidget(self.job_id_input)
        self.download_layout.addWidget(self.download_button)
        self.layout.addLayout(self.download_layout)

        # 按钮：清除任务列表
        self.clear_jobs_button = QtWidgets.QPushButton("Clear Job List")
        self.clear_jobs_button.clicked.connect(self.clear_job_list)
        self.layout.addWidget(self.clear_jobs_button)

    def get_job_list(self):
        # 实现获取任务列表的逻辑
        response = self.send_to_backend('GET', '/jobs')

        if response.status_code == 200:
            jobs = response.json()  
            self.jobs_list_widget.clear()  # 清除旧的列表项
            for job in jobs:
                job_id = job.get('jobid', 'Unknown Job ID')  # 使用 get 方法以防字段不存在
                status = job.get('status', 'No Status')
                original_file = job.get('originaldatafile', 'No File')
                self.jobs_list_widget.addItem(f"Job ID: {job_id}, Status: {status}, File: {original_file}")
        else:
            print("Failed to get job list", response.status_code, response.text)
       

    def download_job_result(self):
        # 实现下载任务结果的逻辑
        job_id = self.job_id_input.text()  
        
        response = self.send_to_backend('GET', f'/downloadspecific/{job_id}')

        if response.status_code == 200:
            image_data = base64.b64decode(response.json()['result_data'])
            original_file_name = response.json().get('filename', f'downloaded_job_{job_id}.jpg')
            
            # 确定保存路径，例如在用户的下载文件夹中
            save_path = os.path.join(os.path.expanduser("~"), "Downloads", original_file_name)

            with open(save_path, 'wb') as file:
                file.write(image_data)
            print(f"Job {job_id} result downloaded successfully")
        else:
            print(f"Failed to download job {job_id} result", response.status_code, response.text)
        

    def clear_job_list(self):
        # 实现清除任务列表的逻辑
        response = self.send_to_backend('DELETE', '/delete')

        if response.status_code == 200:
            self.jobs_list_widget.clear()
            print("Job list cleared successfully")
        else:
            print("Failed to clear job list", response.status_code, response.text)
        
    def send_to_backend(self, method, path):
        url = f'https://bh10b6ejeg.execute-api.us-east-2.amazonaws.com/prod/{path}'
        headers = {'Authorization': f'Bearer {self.token}'}

        #print(f"Token: {self.token}")
        #print(headers)
        


        if method == 'GET':
            response = requests.get(url, headers=headers)
        
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")

        return response

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    job_manager_window = JobManagerWindow()
    job_manager_window.show()
    sys.exit(app.exec_())




