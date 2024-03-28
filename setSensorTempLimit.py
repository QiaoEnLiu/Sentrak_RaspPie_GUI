#zh-tw
# setSensorTempLimit.py
# 「感測器溫度保護」

# 啟用或停用感測器溫度保護
    # 啟用則可設定溫度上限
try:
    import traceback
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout,\
                                 QCheckBox, QPushButton, QMessageBox
    
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
    import PySQL
    from lineEditOnlyInt import lineEditOnlyInt
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

# unit_default = PPV.tempUnitDist[int(PySQL.selectSQL_Reg(regDF = 4, regKey = 0))] # 攝氏、華氏之間的轉換問題
# temp_default = PySQL.selectSQL_Reg(regDF = 4, regKey = 2) # 攝氏、華氏之間的轉換問題
# act_default = int(PySQL.selectSQL_Reg(regDF = 4, regKey = 3))

actLimit = None

# if act_default == 0:
#     actLimit = '無限制'
# elif act_default == 1:
#     actLimit = f'{temp_default}{unit_default}'

font = QFont()
class setSensorTempLimitFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages):
        super().__init__()
        self.title = title
        print(self.title)

        self.sub_pages=sub_pages
        
        title_label = QLabel(self.title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(24)
        title_label.setFont(font)
        # title_label.setStyleSheet(_style)

        font.setPointSize(18)
        # user_label = QLabel(PPV.presentUser.userInfo())
        # user_label.setFont(font)
        # user_label.setStyleSheet(_style)


        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        # main_layout.setSpacing(0) 

        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)

        checkbox_layout = QVBoxLayout()
        self.checkbox = QCheckBox('啟用感測器溫度保護', self)
        self.checkbox.setFont(font)
        self.checkbox.setStyleSheet("QCheckBox::indicator"
                               "{"
                               "width : 24px;"
                               "height : 24px;"
                               "}")
        
        self.checkbox.setChecked(int(PySQL.selectSQL_Reg(4, 3)) == 1)

        
        checkbox_layout.addWidget(self.checkbox)

        setTemp_layout = QHBoxLayout()
        self.setTemp_label = QLabel('溫度設定：')
        self.setTemp_label.setFont(font)
        self.inputTemp = lineEditOnlyInt()
        self.inputTemp.setFont(font)
        self.inputTemp.setEnabled(self.checkbox.isChecked())
        self.tempUnit = QLabel(PPV.tempUnitDist[int(PySQL.selectSQL_Reg(4, 0))])
        self.tempUnit.setFont(font)
        setTemp_layout.addWidget(self.setTemp_label)
        setTemp_layout.addWidget(self.inputTemp)
        setTemp_layout.addWidget(self.tempUnit)

        # # 定義一個 QTimer 用來定期更新時間
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_time)
        # self.timer.start(1000)  # 1秒更新一次

        presentLimitLayout = QVBoxLayout()
        self.presentLimit = QLabel()
        actLimit = '無限制' if int(PySQL.selectSQL_Reg(4, 3)) == 0 else f'{PySQL.selectSQL_Reg(4, 2)} {PPV.tempUnitDist[int(PySQL.selectSQL_Reg(4, 0))]}'
        self.presentLimit.setText(f'目前限制最高溫度：{actLimit}')
        font.setPointSize(16)
        self.presentLimit.setFont(font)
        presentLimitLayout.addWidget(self.presentLimit)

        set_layout = QVBoxLayout()
        set = QPushButton('設定', self)
        font.setPointSize(18)
        set.setFont(font)
        set_layout.addWidget(set)

        main_layout.addLayout(title_layout)
        main_layout.addLayout(checkbox_layout)
        main_layout.addLayout(setTemp_layout)
        main_layout.addLayout(presentLimitLayout)
        main_layout.addLayout(set_layout)

        self.checkbox.stateChanged.connect(lambda: self.inputTemp.setEnabled(self.checkbox.isChecked()))
        set.clicked.connect(self.setTempLimit)


        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{self.title} Index: {self.stacked_widget.count()}')


    
    def setTempLimit(self):
        # print(self.checkbox.text(), ":", self.checkbox.isChecked())
        # print(self.setTemp_label.text(), self.inputTemp.text(), self.tempUnit.text())

        if self.checkbox.isChecked():
            # action = '啟用' if QMessageBox.question(self, self.title, f'設定最高溫度限制：{self.inputTemp.text() + self.tempUnit.text()}\n確定要啟用感測器溫度保護嗎？',
            #                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes else '取消'
            if QMessageBox.question(self, '感測器溫度保護', f'設定限制最高溫度：{self.inputTemp.text()} {self.tempUnit.text()}\
                                    \n確定要啟用感測器溫度保護嗎？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                action = '啟用'
                # 在這裡添加您想要在使用者點擊"Yes"時執行的程式碼
                
                PySQL.updateSQL_Reg(4, 2, self.inputTemp.text()) # 攝氏、華氏之間的轉換問題
                PySQL.updateSQL_Reg(4, 3, 1)

                print("使用者啟用感測器溫度保護")

                # self.presentLimit.setText(f'目前限制最高溫度：{PySQL.selectSQL_Reg(4, 2)} {PPV.tempUnitDist[int(PySQL.selectSQL_Reg(4, 0))]}')
            else:
                action = '取消'

            
        else:

            if QMessageBox.question(self, '感測器溫度保護', f'目前限制最高溫度：{PySQL.selectSQL_Reg(4, 2)} {self.tempUnit.text()}\
                                    \n確定要停用感測器溫度保護嗎？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                action = '停用'
                # 在這裡添加您想要在使用者點擊"Yes"時執行的程式碼
                PySQL.updateSQL_Reg(4, 3, 0)

                print("使用者停用感測器溫度保護")
                # self.presentLimit.setText(f'目前限制最高溫度：無限制')
            else:
                action = '取消'
                
        actLimit = '無限制' if int(PySQL.selectSQL_Reg(4, 3)) == 0 else f'{PySQL.selectSQL_Reg(4, 2)} {PPV.tempUnitDist[int(PySQL.selectSQL_Reg(4, 0))]}'
        self.presentLimit.setText(f'目前限制最高溫度：{actLimit}')

        QMessageBox.information(self, '感測器溫度保護', f'{action}設定')

    # def update_time(self):
    #     temp_default = PySQL.selectSQL_Reg(regDF = 4, regKey = 2)
    #     unit_default = PPV.tempUnitDist[int(PySQL.selectSQL_Reg(regDF = 4, regKey = 0))] # 攝氏、華氏之間的轉換問題
    #     act_default = int(PySQL.selectSQL_Reg(regDF = 4, regKey = 3))
    #     actLimit = '無限制' if act_default == 0 else f'{temp_default} {unit_default}'
    #     self.presentLimit.setText(f'目前限制最高溫度：{actLimit}')

    #     self.tempUnit.setText(unit_default)
        

