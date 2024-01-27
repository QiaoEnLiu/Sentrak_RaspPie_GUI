#zh-tw
# set_RS485.py

#
try:
    import traceback
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton
    from PyQt5.QtGui import QFont
    from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()
class rs485_Frame(QWidget):
    def __init__(self, title, _style, user, stacked_widget, sub_pages):
        super().__init__()
        print(title)

        rs485_layout = QVBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0) 
        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(72)
        title_label.setFont(font)
        title_label.setStyleSheet(_style)
        title_layout.addWidget(title_label)

        font.setPointSize(36)

        # COM Port
        com_layout = QHBoxLayout()
        com_layout.setContentsMargins(0, 0, 0, 0)
        com_layout.setSpacing(0) 
        com_label = QLabel('COM Port:')
        com_label.setFont(font)
        self.com_combo = QComboBox()
        self.com_combo.setFont(font)
        self.populate_com_ports()
        com_layout.addWidget(com_label)
        com_layout.addWidget(self.com_combo)

        # Baud Rate
        baud_layout = QHBoxLayout()
        baud_layout.setContentsMargins(0, 0, 0, 0)
        baud_layout.setSpacing(0) 
        baud_label = QLabel('Baud Rate:')
        baud_label.setFont(font)
        self.baud_combo = QComboBox()
        self.baud_combo.setFont(font)
        self.baud_combo.addItems(['1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200'])
        # 設定預設選項為 '9600'
        default_baud_rate = '9600'
        default_baud_index = self.baud_combo.findText(default_baud_rate)
        self.baud_combo.setCurrentIndex(default_baud_index)
        baud_layout.addWidget(baud_label)
        baud_layout.addWidget(self.baud_combo)

        # Parity
        parity_layout = QHBoxLayout()
        parity_layout.setContentsMargins(0, 0, 0, 0)
        parity_layout.setSpacing(0) 
        parity_label = QLabel('Parity:')
        parity_label.setFont(font)
        self.parity_combo = QComboBox()
        self.parity_combo.setFont(font)
        self.parity_combo.addItems(['None', 'Even', 'Odd', 'Mark', 'Space'])
        # 設定預設選項為 'None'
        default_parity = 'None'
        default_parity_index = self.parity_combo.findText(default_parity)
        self.parity_combo.setCurrentIndex(default_parity_index)
        parity_layout.addWidget(parity_label)
        parity_layout.addWidget(self.parity_combo)

        # Stop Bits
        stop_bits_layout = QHBoxLayout()
        stop_bits_layout.setContentsMargins(0, 0, 0, 0)
        stop_bits_layout.setSpacing(0) 
        stop_bits_label = QLabel('Stop Bits:')
        stop_bits_label.setFont(font)
        self.stop_bits_combo = QComboBox()
        self.stop_bits_combo.setFont(font)
        stop_bits_mapping = {
            '1': QSerialPort.OneStop,
            '1.5': QSerialPort.OneAndHalfStop,
            '2': QSerialPort.TwoStop,
        }
        for stop_bit, stop_bits_enum in stop_bits_mapping.items():
            self.stop_bits_combo.addItem(stop_bit, stop_bits_enum)
        # 設定預設選項為 '1'
        default_stop_bit = '1'
        default_stop_bit_index = self.stop_bits_combo.findText(default_stop_bit)
        self.stop_bits_combo.setCurrentIndex(default_stop_bit_index)
        stop_bits_layout.addWidget(stop_bits_label)
        stop_bits_layout.addWidget(self.stop_bits_combo)

        # Data Bits
        data_bits_layout = QHBoxLayout()
        data_bits_layout.setContentsMargins(0, 0, 0, 0)
        data_bits_layout.setSpacing(0) 
        data_bits_label = QLabel('Data Bits:')
        data_bits_label.setFont(font)
        self.data_bits_combo = QComboBox()
        self.data_bits_combo.setFont(font)
        self.data_bits_combo.addItems(['5', '6', '7', '8'])
        # 設定預設選項為 '8'
        default_data_bits = '8'
        default_data_bits_index = self.data_bits_combo.findText(default_data_bits)
        self.data_bits_combo.setCurrentIndex(default_data_bits_index)
        data_bits_layout.addWidget(data_bits_label)
        data_bits_layout.addWidget(self.data_bits_combo)

        setting_layout = QVBoxLayout()
        setting_layout.setContentsMargins(0, 0, 0, 0)
        setting_layout.setSpacing(0) 
        set_button = QPushButton('設定', self)
        set_button.setFont(font)
        setting_layout.addWidget(set_button)


        # rs485_layout.addLayout(title_layout)
        # rs485_layout.addStretch()
        rs485_layout.addLayout(com_layout)
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
        print('Current Page Index:', self.current_page_index)


    def populate_com_ports(self):
        com_ports = [port.portName() for port in QSerialPortInfo.availablePorts()]
        self.com_combo.addItems(com_ports)
        print('COM Ports:',com_ports)