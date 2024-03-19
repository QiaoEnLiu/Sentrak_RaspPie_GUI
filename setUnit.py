#zh-tw
# setUnit.py
# 「單位」

# 此程式碼為「顯示」底下的「單位」介面
    # 設定溫度及氧氣濃度單位，並回傳給Slaver

try:
    import traceback, minimalmodbus, threading, PySQL
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, \
        QPushButton, QSizePolicy, QRadioButton, QComboBox
    from PyQt5.QtGui import QFont
    import ProjectPublicVariable as PPV
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()

select_tempUnit = int(PySQL.selectSQL_Reg(regDF = 4, regKey = 0))
select_gasUnit = int(PySQL.selectSQL_Reg(regDF = 4, regKey = 4))

class setUnitFrame(QWidget):

    def __init__(self, title, _style, stacked_widget, sub_pages):
        super().__init__()
        print(title)
        self.sub_pages = sub_pages


        # 定義一個 QTimer 用來定期更新時間
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 1秒更新一次


        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(36)
        title_label.setFont(font)
        # title_label.setStyleSheet(_style)

        temperture_label = QLabel('溫度', self)
        temperture_label.setAlignment(Qt.AlignLeft)  
        font.setPointSize(18)
        temperture_label.setFont(font)

        self.celsius_radio = QRadioButton('攝氏')
        self.fahrenheit_radio = QRadioButton('華氏')

        if select_tempUnit==0:
            self.celsius_radio.setChecked(True)
        elif select_tempUnit==1:
            self.fahrenheit_radio.setChecked(True)
        else:
            pass

        font.setPointSize(12)
        self.celsius_radio.setFont(font)
        self.fahrenheit_radio.setFont(font)

        oxygen_label = QLabel('氧氣濃度', self)
        oxygen_label.setAlignment(Qt.AlignLeft)  
        font.setPointSize(18)
        oxygen_label.setFont(font)

        partial_pressure_label = QLabel('氣體分壓', self)
        partial_pressure_label.setAlignment(Qt.AlignLeft)  
        font.setPointSize(12)
        partial_pressure_label.setFont(font)

        self.gas_unit_ComboBox=QComboBox(self)
        self.gas_unit_ComboBox.addItems(PPV.o2_GasUnitDist.values())
        self.gas_unit_ComboBox.setFont(font)
        self.gas_unit_ComboBox.setCurrentText(PPV.o2_GasUnitDist[select_gasUnit])


        dissolve_label = QLabel('溶解', self)
        dissolve_label.setAlignment(Qt.AlignLeft)  
        font.setPointSize(12)
        dissolve_label.setFont(font)


        set=QPushButton('設定', self)
        set.setFont(font)
        # set.setStyleSheet(_style)
        set.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        set.clicked.connect(self.setUnit)
        

        # user_label = QLabel(user.userInfo())
        # user_label.setFont(font)
        # user_label.setStyleSheet(_style)

        setUnit_layout = QVBoxLayout(self)
        setUnit_layout.setContentsMargins(0, 0, 0, 0)
        setUnit_layout.setSpacing(0) 
        setUnit_layout.addWidget(title_label)
        
        temperture_layout = QVBoxLayout()
        temperture_layout.setContentsMargins(10, 10, 10, 10)
        temperture_layout.setSpacing(0) 
        temperture_layout.addWidget(temperture_label)

        tempUnit_layout = QHBoxLayout()
        temperture_layout.setContentsMargins(10, 10, 10, 10)
        tempUnit_layout.addWidget(self.celsius_radio)
        tempUnit_layout.addWidget(self.fahrenheit_radio)
        temperture_layout.addLayout(tempUnit_layout)

        oxygen_layout = QVBoxLayout()
        oxygen_set_layout = QHBoxLayout()
        oxygen_layout.setContentsMargins(10, 10, 10, 10)
        oxygen_layout.setSpacing(0)
        oxygen_layout.addWidget(oxygen_label)
        oxygen_layout.addLayout(oxygen_set_layout)

        o2_pp_layout = QVBoxLayout()
        o2_pp_layout.addWidget(partial_pressure_label)
        o2_pp_layout.addWidget(self.gas_unit_ComboBox)

        o2_dissolve_layout=QVBoxLayout()
        o2_dissolve_layout.addWidget(dissolve_label)

        oxygen_set_layout.addLayout(o2_pp_layout)
        oxygen_set_layout.addLayout(o2_dissolve_layout)

        set_layout = QVBoxLayout()
        set_layout.setContentsMargins(10, 10, 10, 10)
        set_layout.setSpacing(0)
        set_layout.addWidget(set)

        setUnit_layout.addLayout(temperture_layout)
        setUnit_layout.addLayout(oxygen_layout)
        setUnit_layout.addLayout(set_layout)
        
        # setUnit_layout.addWidget(user_label)

        print('顯示溫度測試畫面：', title)

        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{title} Index: {self.stacked_widget.count()}')

    #region
    def update_time(self):
        self.sync()
    
    
    def setUnit(self):
        print('Set Unit')
        if self.celsius_radio.isChecked():
            select_tempUnit = 0  # 攝氏
        elif self.fahrenheit_radio.isChecked():
            select_tempUnit = 1  # 華氏
        else:
            select_tempUnit = -1
        PySQL.updateSQL_Reg(regDF = 4, regKey = 0, updateValue = select_tempUnit)
        PySQL.updateSQL_Reg(regDF = 4, regKey = 4, updateValue = self.gas_unit_ComboBox.currentIndex())

        try:
            PPV.timer.start(1000)
            

            PPV.instrument_ID1.write_register(PPV.R4X_address('Temp unit'), int(PySQL.selectSQL_Reg(regDF = 4, regKey = 0)), functioncode=6)
            PPV.instrument_ID1.write_register(PPV.R4X_address('Set Gas Unit'), int(PySQL.selectSQL_Reg(regDF = 4, regKey = 4)),functioncode=6)
            
            print(f'溫度單位{PPV.tempUnitDist[select_tempUnit]}（{select_tempUnit}），濃度單位{PPV.o2_GasUnitDist[self.gas_unit_ComboBox.currentIndex()]}（{self.gas_unit_ComboBox.currentIndex()}）')
        except minimalmodbus.NoResponseError as e:
            print(f'Set Unit Interface: {e}')
        except Exception as e:
            traceback.print_exc()
            print(f'Exception: {e}')

    def sync(self):

        select_tempUnit = int(PySQL.selectSQL_Reg(regDF = 4, regKey = 0))
        select_gasUnit = int(PySQL.selectSQL_Reg(regDF = 4, regKey = 4))
        
        # try:
        #     modbusTempUnit = PPV.instrument_ID1.read_register(PPV.R4X_address('Temp unit'), functioncode=3)
        #     modbusGasUnit = PPV.instrument_ID1.read_register(PPV.R4X_address('Set Gas Unit'), functioncode=3)
        #     if modbusTempUnit != select_tempUnit:
        #         PPV.instrument_ID1.write_register(PPV.R4X_address('Temp unit'), select_tempUnit, functioncode=6)
        #     if modbusGasUnit != select_gasUnit:
        #         PPV.instrument_ID1.write_register(PPV.R4X_address('Set Gas Unit'), select_gasUnit, functioncode=6)
        # except minimalmodbus.NoResponseError as e:
        #     pass
        # except Exception as e:
        #     traceback.print_exc()
        #     print(f'Exception: {e}')
    #endregion
    