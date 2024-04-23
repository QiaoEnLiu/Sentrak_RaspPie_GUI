#zh-tw
# record_AutoManual.py

# 此程式碼為「記錄」的「記錄方式設定」
try:
    import traceback
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout,QComboBox,QPushButton
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()
class record_AutoManualFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages):
        super().__init__()
        print(title)

        self.sub_pages=sub_pages
        
        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(32)
        title_label.setFont(font)
        # title_label.setStyleSheet(_style)

        font.setPointSize(24)
        # user_label = QLabel(PPV.presentUser.userInfo())
        # user_label.setFont(font)
        # user_label.setStyleSheet(_style)

        self.auto_manual = QComboBox()
        self.auto_manual.setFont(font)
        self.auto_manual.addItems(PPV.setAutoManual.values())
        
        set_button = QPushButton('設定', self)
        set_button.setFont(font)
        # set_button.clicked.connect(self.setPlotTimes)

        set_auto_manual_layout = QVBoxLayout()
        set_auto_manual_layout.addWidget(self.auto_manual)
        set_auto_manual_layout.addStretch()
        set_auto_manual_layout.addWidget(set_button)

        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        # main_layout.setSpacing(0) 
        main_layout.addWidget(title_label)
        # main_layout.addWidget(user_label)
        main_layout.addLayout(set_auto_manual_layout)



        print(f'{title}畫面')

        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{title} Index: {self.stacked_widget.count()}')