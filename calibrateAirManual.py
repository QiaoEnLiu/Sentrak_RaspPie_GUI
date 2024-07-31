#zh-tw
# calibrateAirManual.py

# 此程式碼為「空氣校正」及「直接校正」介面
try:
    import traceback
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox, QPushButton
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()
class calibrateAirManualFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages, mainTitle):
        super().__init__()
        self.title= title
        print(self.title)

        self.sub_pages=sub_pages
        
        title_label = QLabel(self.title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(20)
        title_label.setFont(font)
        # title_label.setStyleSheet(_style)

        font.setPointSize(12)
        # user_label = QLabel(PPV.presentUser.userInfo())
        # user_label.setFont(font)
        # user_label.setStyleSheet(_style)

        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        # main_layout.setSpacing(0) 
        
        
        # main_layout.addWidget(user_label)

        manualLayout=QVBoxLayout()
        manualLabel=QLabel("輸入校正數值：")
        manualLabel.setFont(font)
        self.manualInput = QLineEdit()
        self.manualInput.setFont(font)
        manualLayout.addWidget(manualLabel)
        manualLayout.addWidget(self.manualInput)

        if self.title == "直接校正":
            manualLabel.setEnabled(True)
            self.manualInput.setEnabled(True)
        else:
            manualLabel.setEnabled(False)
            self.manualInput.setEnabled(False)

        

        diaphragmLayout = QVBoxLayout()
        diaphragmLabel = QLabel("膜片：")
        self.diaphragmQCombox = QComboBox()
        self.diaphragmQCombox.addItems(PPV.diaphragm.values())
        diaphragmLabel.setFont(font)
        self.diaphragmQCombox.setFont(font)
        diaphragmLayout.addWidget(diaphragmLabel)
        diaphragmLayout.addWidget(self.diaphragmQCombox)

        actCO2Layout = QVBoxLayout()
        actCO2_Label=QLabel("CO2 Insensitivity:")
        self.actCO2_QCombox=QComboBox()
        self.actCO2_QCombox.addItems(PPV.actCO2_Insensitivity.values())
        actCO2_Label.setFont(font)
        self.actCO2_QCombox.setFont(font)
        actCO2Layout.addWidget(actCO2_Label)
        actCO2Layout.addWidget(self.actCO2_QCombox)

        cali_button = QPushButton('確認', self)
        cali_button.setFont(font)
        # set_button.clicked.connect(self.setLanguage)

        main_layout.addWidget(title_label)
        # main_layout.addWidget(manualLabel)
        # main_layout.addWidget(self.manualInput)
        # main_layout.addWidget(diaphragmLabel)
        # main_layout.addWidget(self.diaphragmQCombox)
        # main_layout.addWidget(actCO2_Label)
        # main_layout.addWidget(self.actCO2_QCombox)
        main_layout.addLayout(manualLayout)
        main_layout.addLayout(diaphragmLayout)
        main_layout.addLayout(actCO2Layout)
        main_layout.addStretch()
        main_layout.addWidget(cali_button)

        # print('終節點測試畫面：', self.title)

        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{self.title} Index: {self.stacked_widget.count()}')