#zh-tw
# calibratePressure.py

# 此程式碼為「大氣壓力校正」
    
try:
    import traceback
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()
class calibratePressureFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages, mainTitle):
        super().__init__()
        print(title)

        self.sub_pages=sub_pages
        
        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(24)
        title_label.setFont(font)
        # title_label.setStyleSheet(_style)

        font.setPointSize(16)
        # user_label = QLabel(PPV.presentUser.userInfo())
        # user_label.setFont(font)
        # user_label.setStyleSheet(_style)

        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        # main_layout.setSpacing(0) 
        
        # main_layout.addWidget(user_label)

        # pressureLayout=QVBoxLayout()
        pressureLabel=QLabel("輸入校正數值：")
        pressureLabel.setFont(font)
        self.pressureInput = QLineEdit()
        self.pressureInput.setFont(font)
        # pressureLayout.addWidget(pressureLabel)
        # pressureLayout.addWidget(self.pressureInput)

        cali_button = QPushButton('確認', self)
        cali_button.setFont(font)

        main_layout.addWidget(title_label)
        main_layout.addWidget(pressureLabel)
        main_layout.addWidget(self.pressureInput)
        main_layout.addStretch()
        main_layout.addWidget(cali_button)

        # print('終節點測試畫面：', title)

        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{title} Index: {self.stacked_widget.count()}')