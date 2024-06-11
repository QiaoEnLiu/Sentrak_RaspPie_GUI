#zh-tw
# setAlarmRelay1.py

# 此程式碼為設定Relay1
    
try:
    import traceback
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, \
        QHBoxLayout, QComboBox, QPushButton, QMessageBox
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
    import PySQL
    from lineEditOnlyInt import lineEditOnlyInt
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

# |0   |1       |2        |3       |
# |狀態|測量類型|接觸點型式|數值判別|
#0|停用|濃度　　|常開　　　|高於　　|
#1|啟用|溫度　　|常關　　　|低於　　|

font = QFont()
class setAlarmRelayFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages):
        super().__init__()
        self.title = title
        # print(self.title.split())
        # print(PySQL.selectAlarmRelay(int(self.title.split()[1])))
        self.relayID = int(self.title.split()[1])
        self.sqlAlarmStatus = PySQL.selectAlarmRelay()[self.relayID]['status']
        if self.sqlAlarmStatus[1] == '0':
            self.sqlAlarmValue = PySQL.selectAlarmRelay()[self.relayID]['value_o2']
        else:
            self.sqlAlarmValue = PySQL.selectAlarmRelay()[self.relayID]['value_temp']
        print(f"暫存狀態碼：{self.sqlAlarmStatus}\r\n暫存數值：{PySQL.selectAlarmRelay()[self.relayID]['value_o2']}（濃度）{PySQL.selectAlarmRelay()[self.relayID]['value_temp']}（溫度）")
        self.sub_pages=sub_pages
        
        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        # title_label.setContentsMargins(0, 0, 0, 0)
        font.setPointSize(20)
        title_label.setFont(font)
        # title_label.setStyleSheet(_style)



        font.setPointSize(16)
        # user_label = QLabel(PPV.presentUser.userInfo())
        # user_label.setFont(font)
        # user_label.setStyleSheet(_style)
        
        #region Relay狀態
        relayStatusLabel = QLabel(f"{title}狀態：")
        relayStatusLabel.setFont(font)
        self.relayStatusCombox = QComboBox()
        self.relayStatusCombox.setFont(font)
        self.relayStatusCombox.addItems(['停用', '啟用'])
        self.relayStatusCombox.setCurrentIndex(int(self.sqlAlarmStatus[0]))
        self.relayStatusDefault=self.relayStatusCombox.currentText()
        #endregion

        #region 測量類型
        meassureTypeLabel = QLabel("測量類型：")
        meassureTypeLabel.setFont(font)
        self.meassureTypeCombox = QComboBox()
        self.meassureTypeCombox.setFont(font)
        self.meassureTypeCombox.addItems(['濃度', '溫度'])
        self.meassureTypeCombox.setCurrentIndex(int(self.sqlAlarmStatus[1]))
        self.meassureTypeDefault=self.meassureTypeCombox.currentText()
        #endregion

        #region 接觸點型式
        switchTypeLabel = QLabel("接觸點型式：")
        switchTypeLabel.setFont(font)
        self.switchTypeCombox = QComboBox()
        self.switchTypeCombox.setFont(font)
        self.switchTypeCombox.addItems(['常開', '常關'])
        self.switchTypeCombox.setCurrentIndex(int(self.sqlAlarmStatus[2]))
        self.switchTypeDefault=self.switchTypeCombox.currentText()
        #endregion

        #region 數值判別
        valueLimitTypeLabel = QLabel("數值判別：")
        valueLimitTypeLabel.setFont(font)
        self.valueLimitTypeCombox = QComboBox()
        self.valueLimitTypeCombox.setFont(font)
        self.valueLimitTypeCombox.addItems(['高於', '低於'])
        self.valueLimitTypeCombox.setCurrentIndex(int(self.sqlAlarmStatus[3]))
        self.valueLimitTypeDefault=self.valueLimitTypeCombox.currentText()
        #endregion

        #region 數值設定
        valueLabel = QLabel("數值：")
        valueLabel.setFont(font)
        self.valueInput = lineEditOnlyInt(self.sqlAlarmValue)
        self.valueInput.setFont(font)
        self.valueDefault = self.valueInput.text()
        #endregion

        set_button = QPushButton('設定', self)
        set_button.setFont(font)
        set_button.clicked.connect(self.setAlarm)


        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0) 
        main_layout.addWidget(title_label)
        # main_layout.addWidget(user_label)

        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.setSpacing(0)
        # title_layout.setContentsMargins(0, 0, 0, 0)

        #region 介面配制
        relayStatusLayout = QHBoxLayout()
        relayStatusLayout.setContentsMargins(10, 10, 10, 10)
        # relayStatusLayout.setSpacing(0)
        relayStatusLeft = QVBoxLayout()
        relayStatusRight = QVBoxLayout()
        relayStatusLeft.addWidget(relayStatusLabel)
        relayStatusRight.addWidget(self.relayStatusCombox)
        relayStatusLayout.addLayout(relayStatusLeft)
        relayStatusLayout.addLayout(relayStatusRight)

        meassureTypeLayout = QHBoxLayout()
        meassureTypeLayout.setContentsMargins(10, 10, 10, 10)
        # meassureTypeLayout.setSpacing(0)
        meassureTypeLeft = QVBoxLayout()
        meassureTypeRight = QVBoxLayout()
        meassureTypeLeft.addWidget(meassureTypeLabel)
        meassureTypeRight.addWidget(self.meassureTypeCombox)
        meassureTypeLayout.addLayout(meassureTypeLeft)
        meassureTypeLayout.addLayout(meassureTypeRight)

        switchTypeLayout = QHBoxLayout()
        switchTypeLabel.setContentsMargins(10, 10, 10, 10)
        # switchTypeLayout.setSpacing(0)
        switchTypeLeft = QVBoxLayout()
        switchTypeRight = QVBoxLayout()
        switchTypeLeft.addWidget(switchTypeLabel)
        switchTypeRight.addWidget(self.switchTypeCombox)
        switchTypeLayout.addLayout(switchTypeLeft)
        switchTypeLayout.addLayout(switchTypeRight)
        
        valueLimitTypeLayout = QHBoxLayout()
        valueLimitTypeLayout.setContentsMargins(10, 10, 10, 10)
        # valueLimitTypeLayout.setSpacing(0)
        valueLimitTypeLeft = QVBoxLayout()
        valueLimitTypeRight = QVBoxLayout()
        valueLimitTypeLeft.addWidget(valueLimitTypeLabel)
        valueLimitTypeRight.addWidget(self.valueLimitTypeCombox)
        valueLimitTypeLayout.addLayout(valueLimitTypeLeft)
        valueLimitTypeLayout.addLayout(valueLimitTypeRight)

        valueLayout = QHBoxLayout()
        valueLayout.setContentsMargins(10, 10, 10, 10)
        # valueLayout.setSpacing(0)
        valueLeft = QVBoxLayout()
        valueRight = QVBoxLayout()
        valueLeft.addWidget(valueLabel)
        valueRight.addWidget(self.valueInput)
        valueLayout.addLayout(valueLeft)
        valueLayout.addLayout(valueRight)


        setLayout = QVBoxLayout()
        setLayout.addWidget(set_button)
        # setLayout.setSpacing(0)

        main_layout.addLayout(title_layout)
        main_layout.addLayout(relayStatusLayout)
        main_layout.addLayout(meassureTypeLayout)
        main_layout.addLayout(switchTypeLayout)
        main_layout.addLayout(valueLimitTypeLayout)
        main_layout.addLayout(valueLayout)
        main_layout.addLayout(setLayout)
        #endregion


        print(f'警報{self.title}測試畫面')

        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{title} Index: {self.stacked_widget.count()}')

    def setAlarm(self):
        setAlarmInfo = f'\r\n' + \
            f'設定{self.title}\r\n' + \
            f'狀態： {self.relayStatusDefault} 改成 {self.relayStatusCombox.currentText()}\r\n' + \
            f'測量類型： {self.meassureTypeDefault} 改成 {self.meassureTypeCombox.currentText()}\r\n' + \
            f'接觸點型式： {self.switchTypeDefault} 改成 {self.switchTypeCombox.currentText()}\r\n' + \
            f'數值判別： {self.valueLimitTypeDefault} 改成 {self.valueLimitTypeCombox.currentText()}\r\n' + \
            f'數值： {self.valueDefault} 改成 {self.valueInput.text()}\r\n'
        
        status = str(self.relayStatusCombox.currentIndex()) + \
            str(self.meassureTypeCombox.currentIndex()) + \
            str(self.switchTypeCombox.currentIndex()) + \
            str(self.valueLimitTypeCombox.currentIndex())
        
        if QMessageBox.question(self, f'設定{self.title}', f'{setAlarmInfo}\
                                \n確定要設定{self.title}嗎？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
            action = '設定'
            # 在這裡添加您想要在使用者點擊"Yes"時執行的程式碼

            PySQL.updateSQL_Reg(1, self.relayID-1, self.relayStatusCombox.currentIndex())
            PySQL.updateAlarmRelay(self.relayID, status, self.valueInput.text())
            print(f"使用者設定{self.title}：{status}\r\n設定數值：{self.valueInput.text()}")
        else:
            action = '取消'
        
        