#zh-tw
# testEndFrame.py

# 此程式碼為子畫面最終刷新測試碼
    # 尚未實作的功能介面都會先以此介面顯示
try:
    import traceback
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout,\
          QDoubleSpinBox, QPushButton, QLineEdit, QComboBox
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
    import PySQL
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()
class setAnalogyOutputFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages):
        super().__init__()
        print(title)

        self.sub_pages=sub_pages
        
        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(24)
        title_label.setFont(font)
        # title_label.setStyleSheet(_style)

        font.setPointSize(14)
        # user_label = QLabel(PPV.presentUser.userInfo())
        # user_label.setFont(font)
        # user_label.setStyleSheet(_style)

        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        # main_layout.setSpacing(0) 
        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)

        state_layout = QHBoxLayout()
        stateLabel_layout = QVBoxLayout()
        stateCombobox_layout = QVBoxLayout()
        stateLabel = QLabel("狀態：")
        self.stateCombox = QComboBox()
        stateLabel.setFont(font)
        self.stateCombox.setFont(font)
        stateLabel_layout.addWidget(stateLabel)
        stateCombobox_layout.addWidget(self.stateCombox)
        state_layout.addLayout(stateLabel_layout)
        state_layout.addLayout(stateCombobox_layout)

        self.stateCombox.addItems(['停用', '啟用'])

        stateOutput_layout = QHBoxLayout()
        stateOutputLabel_layout = QVBoxLayout()
        stateOutputCombobox_layout = QVBoxLayout()
        stateOutputLabel = QLabel("輸出類型：")
        self.stateOutputCombox = QComboBox()
        stateOutputLabel.setFont(font)
        self.stateOutputCombox.setFont(font)
        stateOutputLabel_layout.addWidget(stateOutputLabel)
        stateOutputCombobox_layout.addWidget(self.stateOutputCombox)
        stateOutput_layout.addLayout(stateOutputLabel_layout)
        stateOutput_layout.addLayout(stateOutputCombobox_layout)

        self.stateOutputCombox.addItems(PPV.ct_range.values())
        self.stateOutputCombox.setCurrentText(PPV.ct_range[int(PySQL.selectSQL_Reg(4, 10))])


        stateLow_layout = QHBoxLayout()
        stateLowLabel_layout = QVBoxLayout()
        stateLowSpin_layout = QVBoxLayout()
        stateLowLabel = QLabel(f"低點數值（{PPV.current_Min}-{PPV.current_Max}）：")
        self.stateLowSpin = QDoubleSpinBox()
        stateLowLabel.setFont(font)
        self.stateLowSpin.setFont(font)
        stateLowLabel_layout.addWidget(stateLowLabel)
        stateLowSpin_layout.addWidget(self.stateLowSpin)
        stateLow_layout.addLayout(stateLowLabel_layout)
        stateLow_layout.addLayout(stateLowSpin_layout)

        self.stateLowSpin.setMinimum(PPV.current_Min)
        self.stateLowSpin.setMaximum(PPV.current_Max)
        self.stateLowSpin.setSingleStep(1)
        self.stateLowSpin.setDecimals(0)

        
        stateHigh_layout = QHBoxLayout()
        stateHighLabel_layout = QVBoxLayout()
        stateHighSpin_layout = QVBoxLayout()
        stateHighLabel = QLabel(f"高點數值（{PPV.current_Min}-{PPV.current_Max}）：")
        self.stateHighSpin = QDoubleSpinBox()
        stateHighLabel.setFont(font)
        self.stateHighSpin.setFont(font)
        stateHighLabel_layout.addWidget(stateHighLabel)
        stateHighSpin_layout.addWidget(self.stateHighSpin)
        stateHigh_layout.addLayout(stateHighLabel_layout)
        stateHigh_layout.addLayout(stateHighSpin_layout)

        self.stateHighSpin.setMinimum(PPV.current_Min)
        self.stateHighSpin.setMaximum(PPV.current_Max)
        self.stateHighSpin.setSingleStep(1)
        self.stateHighSpin.setDecimals(0)

        stateTest_layout = QHBoxLayout()
        stateTestLabel_layout = QVBoxLayout()
        stateTestSpin_layout = QVBoxLayout()
        stateTestLabel = QLabel("輸出測試（%）：")
        self.stateTestSpin = QDoubleSpinBox()
        stateTestLabel.setFont(font)
        self.stateTestSpin.setFont(font)
        stateTestLabel_layout.addWidget(stateTestLabel)
        stateTestSpin_layout.addWidget(self.stateTestSpin)
        stateTest_layout.addLayout(stateTestLabel_layout)
        stateTest_layout.addLayout(stateTestSpin_layout)

        self.stateTestSpin.setMinimum(0)
        self.stateTestSpin.setMaximum(100)
        self.stateTestSpin.setSingleStep(1)
        self.stateTestSpin.setDecimals(0)

        setting_layout = QHBoxLayout()
        set = QPushButton("設定")
        set.setFont(font)
        setting_layout.addWidget(set)

        set.clicked.connect(self.setAnalogyOutput)

        main_layout.addLayout(title_layout)
        main_layout.addLayout(state_layout)
        main_layout.addLayout(stateOutput_layout)
        main_layout.addLayout(stateLow_layout)
        main_layout.addLayout(stateHigh_layout)
        main_layout.addLayout(stateTest_layout)
        main_layout.addLayout(setting_layout)

        print('終節點測試畫面：', title)

        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{title} Index: {self.stacked_widget.count()}')

    def setAnalogyOutput(self):
        # print(PPV.fromValueFindKey(PPV.ct_range, self.stateOutputCombox.currentText()))
        PySQL.updateSQL_Reg(4, 10, updateValue = PPV.fromValueFindKey(PPV.ct_range, self.stateOutputCombox.currentText()))