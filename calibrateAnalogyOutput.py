#zh-tw
# calibrateAnalogyOutput.py

# 此程式碼為子畫面最終刷新測試碼
    # 尚未實作的功能介面都會先以此介面顯示
try:
    import traceback
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QDoubleSpinBox, QPushButton
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
    import PySQL
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()

# selectLowValue = int(PySQL.selectSQL_Reg(4, 20))
# selectHighValue = int(PySQL.selectSQL_Reg(4, 21))
class calibrateAnalogyOutputFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages):
        super().__init__()
        self.title=title
        print(self.title)

        self.sub_pages=sub_pages
        
        title_label = QLabel(self.title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(28)
        title_label.setFont(font)
        # title_label.setStyleSheet(_style)

        font.setPointSize(20)
        # user_label = QLabel(PPV.presentUser.userInfo())
        # user_label.setFont(font)
        # user_label.setStyleSheet(_style)

        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        # main_layout.setSpacing(0) 
        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)
        # main_layout.addWidget(user_label)

        lowLimit_layout = QHBoxLayout()
        lowLimit_label=QLabel('低點：')
        lowLimit_label.setFont(font)
        self.lowLimitSpin = QDoubleSpinBox()
        self.lowLimitSpin.setFont(font)
        self.lowLimitSpin.setMinimum(PPV.current_Min)
        self.lowLimitSpin.setMaximum(PPV.current_Man)
        self.lowLimitSpin.setValue(int(PySQL.selectSQL_Reg(4, 20)))
        self.lowLimitSpin.setSingleStep(1)
        self.lowLimitSpin.setDecimals(0)
        lowLimit_layout.addWidget(lowLimit_label)
        lowLimit_layout.addWidget(self.lowLimitSpin)

        highLimit_layout = QHBoxLayout()
        highLimit_label=QLabel('高點：')
        highLimit_label.setFont(font)
        self.highLimitSpin = QDoubleSpinBox()
        self.highLimitSpin.setFont(font)
        self.highLimitSpin.setMinimum(PPV.current_Min) # 設定最小值
        self.highLimitSpin.setMaximum(PPV.current_Max) # 設定最大值
        self.highLimitSpin.setValue(int(PySQL.selectSQL_Reg(4, 21))) # 設定初始值
        self.highLimitSpin.setSingleStep(1) # 設定遞增/遞減的步長
        self.highLimitSpin.setDecimals(0) # 設定小數點後的位數為0
        highLimit_layout.addWidget(highLimit_label)
        highLimit_layout.addWidget(self.highLimitSpin)

        calibrate_layout = QVBoxLayout()
        calibrate = QPushButton('校正', self)
        calibrate.clicked.connect(self.calibrateAnalogy)
        font.setPointSize(18)
        calibrate.setFont(font)
        calibrate_layout.addWidget(calibrate)


        main_layout.addLayout(title_layout)
        main_layout.addLayout(lowLimit_layout)
        main_layout.addLayout(highLimit_layout)
        main_layout.addLayout(calibrate_layout)

        print('測試畫面：', self.title)

        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{self.title} Index: {self.stacked_widget.count()}')
    
    def calibrateAnalogy(self):
        selectLowValue = int(self.lowLimitSpin.value())
        selectHighValue = int(self.highLimitSpin.value())
        # self.lowLimitSpin.setValue(selectLowValue)
        # self.highLimitSpin.setValue(selectHighValue)
        PySQL.updateSQL_Reg(4, 20, selectLowValue)
        PySQL.updateSQL_Reg(4, 21, selectHighValue)

        print(f'{self.title}低點：{selectLowValue}\r\n{self.title}高點：{selectHighValue}')