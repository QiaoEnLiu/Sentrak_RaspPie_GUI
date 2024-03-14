#zh-tw
# setTime.py
# 「時間」

# 此程式碼為設定時間程式碼
    # 尚未實作調整時間
try:
    import traceback, minimalmodbus, threading, PySQL
    from PyQt5.QtCore import Qt, QTimer, QDateTime
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, \
                            QSizePolicy, QRadioButton, QComboBox
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()


# 取得日期格式
date_formats = PPV.dateFormat
# modbusTimeFormat=None
select_Format=None
class setTimeFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages):
        super().__init__()
        print(title)

        self.sub_pages=sub_pages

        self.delayTime = QTimer(self)
        self.delayTime.start(1000)
        # modbusTimeFormat = PPV.instrument_ID1.read_register(PPV.R4X_address('Date Formate'), functioncode=3)
        modbusTimeFormat = int(PySQL.selectSQL_Reg(regDF = 4, regKey = 2))
        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(36)
        title_label.setFont(font)
        # title_label.setStyleSheet(_style)

        font.setPointSize(18)
        timeZone_label = QLabel('調整時間')
        timeZone_label.setFont(font)
        timeZoneContent_label = QLabel('調整時間尚未置入內容')
        timeZoneContent_label.setFont(font)

        timeFormat_label = QLabel('日期格式')
        timeFormat_label.setFont(font)


        # 定義一個 QTimer 用來定期更新時間
        self.timer = QTimer(self)
        self.delayTime = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 1秒更新一次

        # modbusTimeFormat = PPV.instrument_4x.read_register(PPV.R4X_address('Date Formate'), functioncode=3)
        # 格式化當前日期時間並創建 RadioButton
        self.radio_buttons = []
        for format_key, (label, date_format) in date_formats.items():
            radio_button = QRadioButton()
            if modbusTimeFormat==format_key:
                radio_button.setChecked(True)
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
        timeFormat_layout.setContentsMargins(10, 10, 10, 10)
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
        set_layout.setContentsMargins(10, 10, 10, 10)
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

    def update_time(self):
        current_datetime = QDateTime.currentDateTime()
        for index,radio_button in enumerate(self.radio_buttons):
                format_key = index
                label, date_format = date_formats[format_key]
                formatted_datetime = current_datetime.toString(f"{date_format} hh:mm:ss")
                radio_button.setText(f"{formatted_datetime} ({label})")
        # try:
        #     # modbusTimeFormat = PPV.instrument_4x.read_register(PPV.R4X_address('Date Formate'), functioncode=3)
        #     for index,radio_button in enumerate(self.radio_buttons):
        #         format_key = index
        #         label, date_format = date_formats[format_key]
        #         formatted_datetime = current_datetime.toString(f"{date_format} hh:mm:ss")
        #         radio_button.setText(f"{formatted_datetime} ({label})")

        #         # print(f"{formatted_datetime} ({label})")
        # except minimalmodbus.NoResponseError as e:
        #     print(f'Set Time ReadModbus: {e}')
        # except Exception as e:
        #     traceback.print_exc()
        #     print(f'Exception: {e}')
        # try:
        #     def modbus_read_thread():
        #         try:
        #             # modbusTimeFormat = PPV.instrument_4x.read_register(PPV.R4X_address('Date Formate'), functioncode=3)
        #             for index,radio_button in enumerate(self.radio_buttons):
        #                 format_key = index
        #                 label, date_format = date_formats[format_key]
        #                 formatted_datetime = current_datetime.toString(f"{date_format} hh:mm:ss")
        #                 radio_button.setText(f"{formatted_datetime} ({label})")

        #                 # print(f"{formatted_datetime} ({label})")
        #         except minimalmodbus.NoResponseError as e:
        #             print(f'Set Time ReadModbus: {e}')
        #         except Exception as e:
        #             traceback.print_exc()
        #             print(f'Exception: {e}')
        #     # 建立一個新的執行緒並啟動
        #     modbus_thread = threading.Thread(target=modbus_read_thread)
        #     modbus_thread.start()
        # except Exception as e:
        #     traceback.print_exc()
        #     print(f'Exception: {e}')
        

    
    def setTime(self):
        print('Set Time')
        for index,radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                select_Format=index
                print(f'Set Time Format:{date_formats[select_Format]}')
        try:
            
            self.delayTime.start(1000)
            PySQL.updateSQL_Reg(regDF = 4, regKey = 1, updateValue = select_Format)
            print(f"Time Formate SQL Update:{select_Format}")
            PPV.instrument_ID1.write_register(PPV.R4X_address('Date Formate'), select_Format, functioncode=6)
            # self.delayTime.start(1000)
        except minimalmodbus.NoResponseError as e:
            print(f'Set Time Interface: {e}')
        except Exception as e:
            traceback.print_exc()
            print(f'Exception: {e}')

        # def modbus_write_thread():
        #     try:
        #         for index,radio_button in enumerate(self.radio_buttons):
        #             if radio_button.isChecked():
        #                 select_Format=index
        #                 print(f'Set Time Format:{date_formats[select_Format]}')
        #         PPV.instrument_4x.write_register(PPV.R4X_address('Date Formate'),select_Format,functioncode=6)
        #         # self.delayTime.start(1000)
        #     except minimalmodbus.NoResponseError as e:
        #         print(f'Set Time Interface: {e}')
        #     except Exception as e:
        #         traceback.print_exc()
        #         print(f'Exception: {e}')
        # # 建立一個新的執行緒並啟動
        # modbus_thread = threading.Thread(target=modbus_write_thread)
        # modbus_thread.start()