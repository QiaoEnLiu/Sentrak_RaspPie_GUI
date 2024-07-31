#zh-tw

# id_Frame.py
# 「登入身份」

#此介面已取消，或未來改成新增使用者的介面

# 此程式碼為「識別」底下「登入身份」程式碼
    # 「登入身份」為id_LogIn_Fram

try:
    import traceback
    from PyQt5.QtCore import Qt, pyqtSignal
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QMessageBox
    from PyQt5.QtGui import QFont
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()

class id_LogIn_Frame(QWidget):
    login_successful = pyqtSignal(bool)

    def __init__(self, title, _style, stacked_widget, sub_pages, mainTitle): # ,main_window
        super().__init__()
        print('進入畫面：', title)  
        self.sub_pages=sub_pages

         # 標題列
        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0) 
        title_layout.setSpacing(0)
        title_label = QLabel(title, self)
        title_label.setContentsMargins(0, 0, 0, 0)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(18)
        title_label.setFont(font)
        # title_label.setStyleSheet(_style)
        title_layout.addWidget(title_label)
        # title_layout.addStretch(1)

        # 帳號輸入框
        self.username_label = QLabel("帳號:", self)
        self.username_label.setFont(font)
        # self.username_label.setStyleSheet("background-color: lightblue;")
        # self.username_label.setAlignment(Qt.AlignCenter)
        self.username_input = QLineEdit(self)
        self.username_input.setFont(font)
        # self.username_input.setAlignment(Qt.AlignCenter)
        self.username_denial_label = QLabel()
        self.username_denial_label.setFont(font)
        self.username_denial_label.setStyleSheet("color: red;")

        # 密碼輸入框
        self.password_label = QLabel("密碼:", self)
        self.password_label.setFont(font)
        # self.password_label.setAlignment(Qt.AlignCenter)
        self.password_input = QLineEdit(self)
        self.password_input.setFont(font)
        # self.password_input.setAlignment(Qt.AlignCenter)
        self.password_input.setEchoMode(QLineEdit.Password)  # 隱藏輸入的文字
        self.password_denial_label = QLabel()
        self.password_denial_label.setFont(font)
        self.password_denial_label.setStyleSheet("color: red;")

        # font.setPointSize(16)
        # self.login_label = QLabel("登入成功！<p>若要重新登入，請登出再登入。", self)
        # self.login_label.setFont(font)


         # 登入按鈕
        font.setPointSize(12)
        self.login_button = QPushButton("登入", self)
        self.login_button.setFont(font)
        # self.login_button.clicked.connect(self.handle_login)
        
        # 水平佈局1，包含帳號標籤和輸入框
        username_layout = QVBoxLayout()
        username_layout.setContentsMargins(15, 15, 15, 15)
        username_input_layout = QHBoxLayout()
        # username_denial_layout = QHBoxLayout()
        username_input_layout.addWidget(self.username_label)
        username_input_layout.addWidget(self.username_input)
        # username_denial_layout.addWidget(self.username_denial_label)
        username_layout.addLayout(username_input_layout)
        # username_layout.addLayout(username_denial_layout)
        

        # 水平佈局2，包含密碼標籤和輸入框
        password_layout = QVBoxLayout()
        password_layout.setContentsMargins(15, 15, 15, 15)
        password_input_layout = QHBoxLayout()
        # password_denial_layout = QHBoxLayout()
        password_input_layout.addWidget(self.password_label)
        password_input_layout.addWidget(self.password_input)
        # password_denial_layout.addWidget(self.password_denial_label)
        password_layout.addLayout(password_input_layout)
        # password_layout.addLayout(password_denial_layout)

        # loginSuccess_layout = QVBoxLayout()
        # loginSuccess_layout.setContentsMargins(15, 15, 15, 15)
        # loginSuccess_layout.addWidget(self.login_label)


        login_bt_layout = QHBoxLayout()
        login_bt_layout.setContentsMargins(15, 15, 15, 15)
        login_bt_layout.addWidget(self.login_button)

        # 垂直佈局，包含所有元素
        id_LogIn_frame_layout = QVBoxLayout(self)
        # id_LogIn_frame_layout.setContentsMargins(0, 0, 0, 0)
        id_LogIn_frame_layout.setSpacing(0)
        id_LogIn_frame_layout.addLayout(title_layout)
        id_LogIn_frame_layout.addStretch(1)
        id_LogIn_frame_layout.addLayout(username_layout)
        id_LogIn_frame_layout.addLayout(password_layout)
        # id_LogIn_frame_layout.addLayout(loginSuccess_layout)
        # id_LogIn_frame_layout.addStretch(1)
        id_LogIn_frame_layout.addLayout(login_bt_layout)

        # self.login_successful.connect(self.login_successful_callback)
        # self.main_window = main_window  # 添加這行，將 main_window 設定為實例變數

        # self.login_button.setVisible(not self.main_window.logout_button.isVisible())
        # self.username_denial_label.setVisible(False)
        # self.password_denial_label.setVisible(False)
        # self.login_label.setVisible(False)

        # self.main_window.logout_button.clicked.connect(self.logout_button_click)

        # if self.main_window.logout_button.isVisible():
        #     self.username_label.setVisible(False)
        #     self.username_input.setVisible(False)
        #     self.password_label.setVisible(False)
        #     self.password_input.setVisible(False)
        #     self.login_label.setVisible(True)
        #     self.login_button.setVisible(False)
        # else:
        #     self.username_label.setVisible(True)
        #     self.username_input.setVisible(True)
        #     self.password_label.setVisible(True)
        #     self.password_input.setVisible(True)
        #     self.login_label.setVisible(False)
        #     self.login_button.setVisible(True)

            
        # print("Connected handle_login_success to login_successful signal.")
        self.stacked_widget = stacked_widget
        id_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = id_frame_index # 將當前的畫面索引設為 plot_page_index

        print(f'{title} Index: {self.stacked_widget.count()}')
        
    def login_successful_callback(self, checkLogin):
        # print('login_successful signal received in id_LogIn_Frame:', checkLogin)
        self.main_window.handle_login_success(checkLogin)

    def handle_login(self):
        # 處理登入按鈕點擊事件的邏輯
        username = self.username_input.text()
        password = self.password_input.text()

        user_P001 = 'Ayt001' #最高權限使用者測試
        pw_P001 = 'Priorty001'

        if username != user_P001:
            self.username_denial_label.setVisible(True)
            print('帳號錯誤！')
            QMessageBox.critical(self, '登入失敗', '帳號錯誤！')
        else:
            self.username_denial_label.setVisible(False)
            if password != pw_P001:
                self.password_denial_label.setVisible(True)
                QMessageBox.critical(self, '登入失敗', '密碼錯誤！')
                print('密碼錯誤！')
            elif password == pw_P001:

                self.username_label.setVisible(False)
                self.username_input.setVisible(False)
                self.password_label.setVisible(False)
                self.password_input.setVisible(False)
                self.login_label.setVisible(True)
                self.login_button.setVisible(False)
                self.login_label.setText(username + self.login_label.text())
                self.password_denial_label.setVisible(False)
                QMessageBox.information(self, '登入成功', self.login_label.text())

                print('正確！')


                # 信號和槽的連接信息
                loginSuccessful = True
                self.login_successful_callback(loginSuccessful)
                self.login_button.setVisible(not self.main_window.logout_button.isVisible())
                self.main_window.logout_button.clicked.connect(self.logout_button_click)

        # print(f"Username: {username}, Password: {password}")

    def logout_button_click(self):
        self.username_label.setVisible(True)
        self.username_input.setVisible(True)
        self.password_label.setVisible(True)
        self.password_input.setVisible(True)
        self.login_label.setVisible(False)
        self.login_button.setVisible(True)
        self.login_button.setVisible(not self.main_window.logout_button.isVisible())

