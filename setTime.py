#zh-tw
# setTime.py
# 「時間」

# 此程式碼為設定時間程式碼
    # 尚未實作調整時間
try:
    import traceback, PySQL
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, \
                            QSizePolicy, QRadioButton, QMessageBox
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
    import PySQL
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()


# 取得日期格式
date_formats = PPV.dateFormat
# setTimeFormat = None
# select_Format = None

class setTimeFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages):
        super().__init__()
        print(title)

        self.sub_pages=sub_pages

        # select_Format = int(PySQL.selectSQL_Reg(regDF = 4, regKey = 1))

        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(20)
        title_label.setFont(font)
        # title_label.setStyleSheet(_style)

        font.setPointSize(16)
        timeZone_label = QLabel('調整時間')
        timeZone_label.setFont(font)
        timeZoneContent_label = QLabel('調整時間尚未置入內容')
        timeZoneContent_label.setFont(font)

        timeFormat_label = QLabel('日期格式')
        timeFormat_label.setFont(font)


        # 定義一個 QTimer 用來定期更新時間
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 1秒更新一次

        # self.timer = QTimer(self)

        # modbusTimeFormat = PPV.instrument_4x.read_register(PPV.R4X_address('Date Formate'), functioncode=3)
        # 格式化當前日期時間並創建 RadioButton
        self.radio_buttons = []
        for format_key, (label, date_format) in date_formats.items():
            radio_button = QRadioButton()

            label, date_format = date_formats[format_key]
            formatted_datetime = f"{date_format} hh:mm:ss"
            radio_button.setText(f"{formatted_datetime} ({label})") 

            if int(PySQL.selectSQL_Reg(4, 1)) == format_key:
                radio_button.setChecked(True)
                self.defaultFormatName = label
            else:
                radio_button.setChecked(False)
            radio_button.setFont(font)
            self.radio_buttons.append(radio_button)
        
        set=QPushButton('設定')
        set.setFont(font)
        # set.setStyleSheet(_style)
        set.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        set.clicked.connect(self.setTime)


        setTime_layout = QVBoxLayout(self)
        setTime_layout.setContentsMargins(0, 0, 0, 0)
        # setTime_layout.setSpacing(0) 
        setTime_layout.addWidget(title_label)

        timeZone_layout = QVBoxLayout()
        timeZone_layout.setContentsMargins(10, 10, 10, 10)
        timeZone_layout.setSpacing(0)

        
        timeZone_layout.addWidget(timeZone_label)
        timeZone_layout.addWidget(timeZoneContent_label)

        timeFormat_layout = QVBoxLayout()
        #timeFormat_layout.setContentsMargins(10, 10, 10, 10)
        timeFormat_layout.setSpacing(0)

        timeFormat_layout.addWidget(timeFormat_label)

        timeRB_layout = QVBoxLayout()
        timeRB_layout.setContentsMargins(0, 0, 0, 0)
        timeRB_layout.setSpacing(0)
        timeRB_layout.setAlignment(Qt.AlignCenter)

        for i in self.radio_buttons:
            timeRB_layout.addWidget(i)
        timeFormat_layout.addLayout(timeRB_layout)

        set_layout = QVBoxLayout()
        #set_layout.setContentsMargins(10, 10, 10, 10)
        set_layout.setSpacing(0)

        set_layout.addWidget(set)

        setTime_layout.addLayout(timeZone_layout)
        setTime_layout.addLayout(timeFormat_layout)
        setTime_layout.addLayout(set_layout)

        print('設定時間測試畫面：', title)

        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{title} Index: {self.stacked_widget.count()}')

    #region
    def update_time(self):
        # select_Format = int(PySQL.selectSQL_Reg(regDF = 4, regKey = 1))
        current_datetime = PPV.current_datetime
        for index,radio_button in enumerate(self.radio_buttons):
            format_key = index
            label, date_format = date_formats[format_key]
            formatted_datetime = current_datetime.toString(f"{date_format} hh:mm:ss")
            radio_button.setText(f"{formatted_datetime} ({label})")
        self.sync()
               

    def setTime(self):
        print('Set Time')
        for index,radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                select_Format=index
                print(f'Set Time Format:{date_formats[select_Format]}')

        if QMessageBox.question(self, '設定時間', f'設定格式：由 {self.defaultFormatName} 改成 {date_formats[select_Format][0]}\
                                \n確定要設定時間嗎？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
            action = '設定'
            # 在這裡添加您想要在使用者點擊"Yes"時執行的程式碼
            
            PySQL.updateSQL_Reg(regDF = 4, regKey = 1, updateValue = select_Format)
            self.defaultFormatName = date_formats[select_Format][0]

            print("使用者設定波形圖週期")

        else:
            action = '取消'
        # self.sync()
        # try:
            
        #     PPV.timer.start(1000)
            
        #     # print(f"Time Formate SQL Update:{select_Format}")
        #     PPV.instrument_ID1.write_register(PPV.R4X_address('Date Formate'), int(PySQL.selectSQL_Reg(regDF = 4, regKey = 1)), functioncode=6)
        # except minimalmodbus.NoResponseError as e:
        #     print(f'Set Time Interface: {e}')
        # except Exception as e:
        #     traceback.print_exc()
        #     print(f'Exception: {e}')

    def sync(self):
        select_Format = int(PySQL.selectSQL_Reg(regDF = 4, regKey = 1))
        
        # try:
        #     modbusTimeFormat = PPV.instrument_ID1.read_register(PPV.R4X_address('Date Formate'), functioncode=3)
        #     if modbusTimeFormat != setTimeFormat:
        #         PPV.instrument_ID1.write_register(PPV.R4X_address('Date Formate'), setTimeFormat, functioncode=6)
        # except minimalmodbus.NoResponseError as e:
        #     pass
        # except Exception as e:
        #     traceback.print_exc()
        #     print(f'Exception: {e}')
    #endregion 
