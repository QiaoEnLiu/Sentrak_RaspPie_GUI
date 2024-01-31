#zh-tw
# testEndFrame.py

#此程式碼為子畫面最終刷新測試碼
#--第一子畫面最終測試碼執行結果 Sentrak_RaspberryPie_GUI.py -> menuSubFrame.py
#--最新最子畫面最終測試碼執行結果 menuSubFrame.py -> testEndFrame.py
try:
    import traceback, minimalmodbus, threading
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, \
        QPushButton, QSizePolicy, QRadioButton, QComboBox
    from PyQt5.QtGui import QFont
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()

tempUnit_address=0
tempUnitDist={0:'°C',1:'°F'}
select_tempUnit=None

o2_GasUnit_address=4
o2_GasUnitDist={0:'ppb',1:'PPM',2:'mg/l',3:'PPMV',4:'%',5:'PPM',6:'mg/l',7:'ppb',8:'PPMV',9:'kPa'}


class setUnitFrame(QWidget):
    def __init__(self, title, _style, user, stacked_widget, sub_pages,it_4x):
        super().__init__()
        print(title)
        self.sub_pages=sub_pages
        self.it_4x=it_4x[0]

        self.temp_unit = self.it_4x.read_register(tempUnit_address,functioncode=3)
        self.setGasUnit = self.it_4x.read_register(o2_GasUnit_address,functioncode=3)
        
        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(72)
        title_label.setFont(font)
        title_label.setStyleSheet(_style)

        temperture_label = QLabel('溫度', self)
        temperture_label.setAlignment(Qt.AlignLeft)  
        font.setPointSize(36)
        temperture_label.setFont(font)

        self.celsius_radio = QRadioButton('攝氏')
        self.fahrenheit_radio = QRadioButton('華氏')

        if self.temp_unit==0:
            self.celsius_radio.setChecked(True)
        elif self.temp_unit==1:
            self.fahrenheit_radio.setChecked(True)
        else:
            pass

        font.setPointSize(24)
        self.celsius_radio.setFont(font)
        self.fahrenheit_radio.setFont(font)

        oxygen_label = QLabel('氧氣濃度', self)
        oxygen_label.setAlignment(Qt.AlignLeft)  
        font.setPointSize(36)
        oxygen_label.setFont(font)

        partial_pressure_label = QLabel('氣體分壓', self)
        partial_pressure_label.setAlignment(Qt.AlignLeft)  
        font.setPointSize(24)
        partial_pressure_label.setFont(font)

        self.gas_unit_ComboBox=QComboBox(self)
        self.gas_unit_ComboBox.addItems(o2_GasUnitDist.values())
        self.gas_unit_ComboBox.setFont(font)
        self.gas_unit_ComboBox.setCurrentText(o2_GasUnitDist[self.setGasUnit])

        dissolve_label = QLabel('溶解', self)
        dissolve_label.setAlignment(Qt.AlignLeft)  
        font.setPointSize(24)
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
        print('Current Page Index:', self.current_page_index)

        # #region 更新日期時間並持續讓modbus讀取資料進圖表    
        # self.timer = QTimer(self) # 更新日期時間的 QTimer
        # self.timer.timeout.connect(self.update_modbus_data)
        # self.timer.start(1000)  # 每秒更新一次




    #region modbus RTU讀取（氧氣濃度、溫度）
    # def update_modbus_data(self):
    #     try:
    #         # 定義一個函數，用於在執行緒中執行Modbus讀取
    #         def modbus_read_thread():
    #             try:
    #                 # 讀取浮點數值，地址為1
    #                 temp_unit = self.it_4x.read_register(tempUnit_address,functioncode=3)
    #                 setGasUnit = self.it_4x.read_register(o2_GasUnit_address,functioncode=3)

    #                 if temp_unit==0:
    #                     self.celsius_radio.setChecked(True)
    #                 elif temp_unit==1:
    #                     self.fahrenheit_radio.setChecked(True)
    #                 else:
    #                     pass

    #                 self.gas_unit_ComboBox.setCurrentText(o2_GasUnitDist[setGasUnit])

    #                 print(f'溫度單位{tempUnitDist[temp_unit]}（{temp_unit}），濃度單位{o2_GasUnitDist[setGasUnit]}（{setGasUnit}）')
    #             except minimalmodbus.NoResponseError as e:
    #                 print(f'Set Unit Interface: {e}')
    #             except Exception as e:
    #                 traceback.print_exc()
    #                 print(f'Exception: {e}')

    #         # 建立一個新的執行緒並啟動
    #         modbus_thread = threading.Thread(target=modbus_read_thread)
    #         modbus_thread.start()
    #     except Exception as e:
    #         traceback.print_exc()
    #         print(f'Exception: {e}')

    #endregion
            
    #region
    def setUnit(self):
        print('Set Unit')
        try:
            
            self.it_4x.write_register(o2_GasUnit_address,self.gas_unit_ComboBox.currentIndex(),functioncode=6)

            if self.celsius_radio.isChecked():
                select_tempUnit = 0  # 攝氏
            elif self.fahrenheit_radio.isChecked():
                select_tempUnit = 1  # 華氏
            else:
                select_tempUnit = -1

            self.it_4x.write_register(tempUnit_address,select_tempUnit,functioncode=6)


            print(f'溫度單位{tempUnitDist[select_tempUnit]}（{select_tempUnit}），濃度單位{o2_GasUnitDist[self.gas_unit_ComboBox.currentIndex()]}（{self.gas_unit_ComboBox.currentIndex()}）')
        except minimalmodbus.NoResponseError as e:
            print(f'Set Unit Interface: {e}')
        except Exception as e:
            traceback.print_exc()
            print(f'Exception: {e}')
    #endregion
    