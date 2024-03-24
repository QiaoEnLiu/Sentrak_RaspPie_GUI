#zh-tw
# set_RS485.py
# 「rs-485」

# 此程式碼為「設定」底下進入「rs-485」並實作Slaver設定的介面
    # 尚未能直接設定Slaver通訊

# |-8     |-7     |-6   |-5   |-4|-3|-2|-1       |
# |Byte                                          |
# |7      |6      |5    |4    |3 |2 |1 |0        |
# |DataBit|StopBit|ParityBits |BaudRate|act/deact|

try:
    import traceback, PySQL
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QRadioButton
    from PyQt5.QtGui import QFont
    # from PyQt5.QtSerialPort import QSerialPort
    import ProjectPublicVariable as PPV
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()

select_RS485_state = int(PySQL.selectSQL_Reg(regDF = 4, regKey = 9))
bin_RS485_state = PPV.d2b(select_RS485_state).zfill(8)
class rs485_Frame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages):
        super().__init__()
        self.title=title
        print(self.title)
        print(f"{self.title}:{select_RS485_state}({bin_RS485_state})")

        # 定義一個 QTimer 用來定期更新時間
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 1秒更新一次

        rs485_layout = QVBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0) 
        self.title_label = QLabel(self.title)
        self.title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(28)
        self.title_label.setFont(font)
        # title_label.setStyleSheet(_style)
        title_layout.addWidget(self.title_label)

        font.setPointSize(18)

        # COM Port
        #暫以本機端通訊埠顯示
        # com_layout = QHBoxLayout()
        # com_layout.setContentsMargins(0, 0, 0, 0)
        # com_layout.setSpacing(0) 
        # com_label = QLabel('COM Port:')
        # com_label.setFont(font)
        # self.com_combo = QComboBox()
        # self.com_combo.setFont(font)
        # self.populate_com_ports()
        # com_layout.addWidget(com_label)
        # com_layout.addWidget(self.com_combo)

        state_layout = QHBoxLayout()
        state_layout.setContentsMargins(0, 0, 0, 0)
        state_layout.setSpacing(0) 
        state_label = QLabel('狀態：')
        state_label.setFont(font)

        
        self.deactivate_radio = QRadioButton('停用')
        # self.deactivate_radio.setChecked(True)
        self.activate_radio = QRadioButton('啟用')
        self.deactivate_radio.setFont(font)
        self.activate_radio.setFont(font)

        # |-1       |
        # |0        |
        # |act/deact|
        if bin_RS485_state[-1:-2]==PPV.stateRS485['停用']:
            self.deactivate_radio.setChecked(True)
        else:
            self.activate_radio.setChecked(True)

        state_layout.addWidget(state_label)
        state_layout.addWidget(self.deactivate_radio)
        state_layout.addWidget(self.activate_radio)

        
        baud_layout = QHBoxLayout()
        baud_layout.setContentsMargins(0, 0, 0, 0)
        baud_layout.setSpacing(0) 
        baud_label = QLabel('Baud Rate:')
        baud_label.setFont(font)
        self.baud_combo = QComboBox()
        self.baud_combo.setFont(font)
        # self.baud_combo.addItems(['1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200'])
        self.baud_combo.addItems(PPV.baudRate.keys())
        # print(PPV.baudRate.keys())

        # Baud Rate
        # |-4|-3|-2|-1
        # |3 |2 |1 |
        # |BaudRate|
        default_baud_rate = PPV.get_keys_from_value(PPV.baudRate, bin_RS485_state[-4:-1])[0]
        default_baud_index = self.baud_combo.findText(default_baud_rate)
        self.baud_combo.setCurrentIndex(default_baud_index)
        baud_layout.addWidget(baud_label)
        baud_layout.addWidget(self.baud_combo)

        
        parity_layout = QHBoxLayout()
        parity_layout.setContentsMargins(0, 0, 0, 0)
        parity_layout.setSpacing(0) 
        parity_label = QLabel('Parity:')
        parity_label.setFont(font)
        self.parity_combo = QComboBox()
        self.parity_combo.setFont(font)
        # self.parity_combo.addItems(['None', 'Odd', 'Even']) # 'Mark', 'Space'

        # Parity
        # |-6   |-5   |-4
        # |5    |4    |
        # |ParityBits |
        self.parity_combo.addItems(PPV.parityBit.keys())
        default_parity = PPV.get_keys_from_value(PPV.parityBit, bin_RS485_state[-6:-4])[0]
        default_parity_index = self.parity_combo.findText(default_parity)
        self.parity_combo.setCurrentIndex(default_parity_index)
        parity_layout.addWidget(parity_label)
        parity_layout.addWidget(self.parity_combo)

        # Stop Bits
        # |-7     |-6
        # |6      |
        # |StopBit|
        stop_bits_layout = QHBoxLayout()
        stop_bits_layout.setContentsMargins(0, 0, 0, 0)
        stop_bits_layout.setSpacing(0) 
        stop_bits_label = QLabel('Stop Bits:')
        stop_bits_label.setFont(font)
        self.stop_bits_combo = QComboBox()
        self.stop_bits_combo.setFont(font)
        # stop_bits_mapping = {
        #     '1': QSerialPort.OneStop,
        #     # '1.5': QSerialPort.OneAndHalfStop,
        #     '2': QSerialPort.TwoStop,
        # }
        # for stop_bit, stop_bits_enum in stop_bits_mapping.items():
        #     self.stop_bits_combo.addItem(stop_bit, stop_bits_enum)
        # self.stop_bits_combo.addItems(['1', '2'])
        self.stop_bits_combo.addItems(PPV.stopBit.keys())
        
        default_stop_bit = PPV.get_keys_from_value(PPV.stopBit, bin_RS485_state[-7:-6])[0]
        default_stop_bit_index = self.stop_bits_combo.findText(default_stop_bit)
        self.stop_bits_combo.setCurrentIndex(default_stop_bit_index)
        stop_bits_layout.addWidget(stop_bits_label)
        stop_bits_layout.addWidget(self.stop_bits_combo)

        
        data_bits_layout = QHBoxLayout()
        data_bits_layout.setContentsMargins(0, 0, 0, 0)
        data_bits_layout.setSpacing(0) 
        data_bits_label = QLabel('Data Bits:')
        data_bits_label.setFont(font)
        self.data_bits_combo = QComboBox()
        self.data_bits_combo.setFont(font)
        # self.data_bits_combo.addItems(['7', '8'])
        self.data_bits_combo.addItems(PPV.dataBit.keys())

        # Data Bits
        # |-8     |-7
        # |7      |
        # |DataBit|
        default_data_bits = PPV.get_keys_from_value(PPV.dataBit, bin_RS485_state[-8:-7])[0]
        default_data_bits_index = self.data_bits_combo.findText(default_data_bits)
        self.data_bits_combo.setCurrentIndex(default_data_bits_index)
        data_bits_layout.addWidget(data_bits_label)
        data_bits_layout.addWidget(self.data_bits_combo)

        setting_layout = QVBoxLayout()
        setting_layout.setContentsMargins(0, 0, 0, 0)
        setting_layout.setSpacing(0) 
        set_button = QPushButton('設定', self)
        set_button.setFont(font)
        set_button.clicked.connect(self.slaverConnect)
        setting_layout.addWidget(set_button)


        # rs485_layout.addLayout(title_layout)
        # rs485_layout.addStretch()
        rs485_layout.addLayout(state_layout)
        rs485_layout.addStretch()
        rs485_layout.addLayout(baud_layout)
        rs485_layout.addStretch()
        rs485_layout.addLayout(parity_layout)
        rs485_layout.addStretch()
        rs485_layout.addLayout(stop_bits_layout)
        rs485_layout.addStretch()
        rs485_layout.addLayout(data_bits_layout)
        rs485_layout.addStretch()
        rs485_layout.addLayout(setting_layout)
        rs485_layout.addStretch()

        # 整體佈局
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(title_layout)
        main_layout.addLayout(rs485_layout)

        print('RS485測試畫面：', title)

        self.sub_pages=sub_pages
        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{title} Index: {self.stacked_widget.count()}')


    # def populate_com_ports(self):
    #     com_ports = [port.portName() for port in QSerialPortInfo.availablePorts()]
    #     self.com_combo.addItems(com_ports)
    #     print('COM Ports:',com_ports)

    def slaverConnect(self):
        # com_port = self.com_combo.currentText()

        if self.deactivate_radio.isChecked():
            stateStr = self.deactivate_radio.text()
            state = PPV.stateRS485[self.deactivate_radio.text()]  # 停用
        elif self.activate_radio.isChecked():
            stateStr = self.activate_radio.text()
            state = PPV.stateRS485[self.activate_radio.text()]  # 啟用
        else:
            stateStr = self.activate_radio.text()
            state = '1'

        baud_rate = self.baud_combo.currentText()
        parity_text = self.parity_combo.currentText()
        stop_bits = self.stop_bits_combo.currentText()
        data_bits = self.data_bits_combo.currentText()


        stateValue = PPV.dataBit[data_bits] + \
            PPV.stopBit[stop_bits] + \
            PPV.parityBit[parity_text] + \
            PPV.baudRate[baud_rate] + \
            state
        

        slaver_Connect_Info=f'\r\n' + \
            f'{self.title}\r\n'+ \
            f'Connect: {stateStr}({state})\r\n' +  \
            f'Baud Rate: {baud_rate}({PPV.baudRate[baud_rate]})\r\n' + \
            f'Parity: {parity_text}({PPV.parityBit[parity_text]})\r\n' + \
            f'Stop Bits: {stop_bits}({PPV.stopBit[stop_bits]})\r\n' + \
            f'Data Bits: {data_bits}({PPV.dataBit[data_bits]})\r\n' + \
            f'RegValue: {PPV.b2d(stateValue)}({stateValue})\r\n'
        
        PySQL.updateSQL_Reg(regDF = 4, regKey = 9, updateValue = PPV.b2d(stateValue))

        print(slaver_Connect_Info)

        # print(f"{self.title}:{select_RS485_state}({bin_RS485_state})")

    def update_time(self):
        select_RS485_state = int(PySQL.selectSQL_Reg(regDF = 4, regKey = 9))
        bin_RS485_state = PPV.d2b(select_RS485_state).zfill(8)
        self.title_label.setText(f"{self.title}:{str(select_RS485_state)}({bin_RS485_state})")
        # print(self.title_label.text())
