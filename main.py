#zh-tw

# main.py
# 此程式碼為主畫面，顯示折線圖為主
# 由於介面往上堆疊，排除初始化介面，折線圖為第一層，進入主選單為第二層，主選單後進入各個子選單為第三層
    # 介面順序由下而上疊：self.plot_canvas/self.menu_page/self.menuSub_page


try:
    
    import sys, os, traceback, minimalmodbus, threading, platform, serial
    # sys.path.append("venv-py3_9/Lib/site-packages")
    # print(sys.path)

    

    from PyQt5.QtWidgets import \
        QApplication, QMainWindow, QWidget, QStatusBar, QVBoxLayout,\
        QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QFrame, QGridLayout,\
        QPushButton, QStackedWidget, QMessageBox, QDesktopWidget\
        
    from PyQt5.QtCore import Qt, QDateTime
    from PyQt5.QtGui import QFont
    from imgResource import setButtonIcon, setLabelIcon, \
        stateAlarm_icons, stateWire_icons, stateRecord_icons\
        ,stateBatteryCharge_icons ,stateBattery_icons ,stateInbMenu_icons, lock_icons

    # from modbus_RTU_Connect_GUI import ModbusRTUConfigurator
    import ProjectPublicVariable as PPV
    import PySQL

    from unit_transfer import unit_transfer
    from plotCanvas import plotCanvas #圖表內部配制
    from subMenuFrame import subMenuFrame #子選單內部配制
    # from img_to_base64 import image_to_base64
    from login import LoginDialog


except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

print(platform.system())


# response = requests.get('http://localhost:5000')
# if response.status_code == 200:
#     print('Flask API啟用')
# else:
#     print('Flask API未啟用')
    
#region 其他全域變數

font = QFont()
font2 = QFont()

spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
spacer_right = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
spacer_left = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)


# modbusTempUnit, sqlTempUnit = 0, 0
# modbusDateFormat, sqlDateFormat = 0, 0

# modbusGasUnit, sqlGasUnit = 0, 0


# dateFormateIndex=2
format_wedget = None
# oxygen_concentration = 0.00 # 12.56
temperature_unit_text='Celsius' # Celsius, Fahrenheit
temperature_unit_default='°C'
# temperature = 0.00 # 攝氏 16.8

#endregion

#class MyWindow
#region 主畫面
class MyWindow(QMainWindow):
    # for i in PySQL.selectAlarmRelay():
    #     for j in i:
    #         print(j)
    # print(PySQL.selectAlarmRelay()[1])
    # print(PySQL.selectAlarmRelay(1))
    # print(PySQL.selectAlarmRelay(2))
    # print(PySQL.selectAlarmRelay(3))
    #region 主畫面元件
    def __init__(self):
        super().__init__()
        PPV.start_flask_api() # 啟動Flask API
        # 設定視窗標題
        self.setWindowTitle("Sentrak_RaspPie_GUI")

        self.isLogin=False

        self.oxygen_concentration = 0.00 # 16712.32767
        self.temperature = 0.00 # 16774.26214


        self.sqlTempUnit = 0
        self.sqlDateFormat = 0

        self.sqlGasUnit = 0

        #region 視窗大小

        # 設置主視窗的尺寸
        # 取得螢幕解析度
        screen_resolution = QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen_resolution.width(), screen_resolution.height()

        # 如果解析度為1920*1080，則全螢幕，否則使用固定解析度
        if screen_width == 800 and screen_height == 480:
            self.showFullScreen()
        else:
            self.setFixedSize(800, 480)
            print()

        window_size = self.size()
        winWidth = window_size.width()
        winHeight = window_size.height()

        print('視窗大小：', winWidth, '*', winHeight)
        print('螢幕解析：', screen_width, '*', screen_height)

        #endregion


        # 創建狀態列
        #region 狀態列
        font.setPointSize(14)
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)
        status_bar.setGeometry(0, 0, 800, 40)  # 設置狀態列的尺寸
        status_bar.setStyleSheet("QStatusBar {background-color: white; padding: 0; margin: 0;}")  # 設置背景顏色
        status_bar.setStyleSheet(status_bar.styleSheet() + "QStatusBar::item{border: 0px}")
        status_bar.setSizeGripEnabled(False)  # 隱藏右下角的調整大小的三角形
        status_bar.setContentsMargins(0, 0, 0, 0)

        self.alarmNull_label = QLabel('無警告', self)
        self.alarmNull_label.setAlignment(Qt.AlignLeft)
        self.alarmNull_label.setStyleSheet("QLabel { border: none; padding: 0; margin: 0;background: transparent;}")
        self.alarmNull_label.setFont(font)
        setLabelIcon(self.alarmNull_label, stateAlarm_icons[0])
        
        self.alarm1_label = QLabel('警告1', self)
        self.alarm1_label.setAlignment(Qt.AlignLeft)
        self.alarm1_label.setStyleSheet("QLabel { border: none; padding: 0; margin: 0;background: transparent;}")
        self.alarm1_label.setFont(font)
        self.alarm1_label.setVisible(False)
        setLabelIcon(self.alarm1_label, stateAlarm_icons[1])

        self.alarm2_label = QLabel('警告2', self)
        self.alarm2_label.setAlignment(Qt.AlignLeft)
        self.alarm2_label.setStyleSheet("QLabel { border: none; padding: 0; margin: 0;background: transparent;}")
        self.alarm2_label.setFont(font)
        self.alarm2_label.setVisible(False)
        setLabelIcon(self.alarm2_label, stateAlarm_icons[2])


        # 在狀態列中央加入日期時間
        self.datetime = QLabel(self)
        self.datetime.setAlignment(Qt.AlignCenter| Qt.AlignCenter)  # 文字置中
        # self.datetime=QPushButton(self)
        # self.datetime.setFlat(True)
        self.datetime.setStyleSheet("QLabel { border: none; padding: 0;  margin: 0;background: transparent;}")
        # self.datetime.setStyleSheet("padding: 0; margin: 0;")
        self.datetime.setFont(font)
        # self.datetime.clicked.connect(self.datetimeFormatChange)

        self.stateUSB_label = QLabel('USB', self)
        self.stateUSB_label.setStyleSheet("QLabel { border: none; padding: 0;  margin: 0;background: transparent;}")
        self.stateUSB_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.stateUSB_label.setFont(font)
        setLabelIcon(self.stateUSB_label, stateWire_icons[2])


        self.stateBattery_label = QLabel('電池', self)
        self.stateBattery_label.setStyleSheet("QLabel { border: none; padding: 0;  margin: 0;background: transparent;}")
        self.stateBattery_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.stateBattery_label.setFont(font)
        setLabelIcon(self.stateBattery_label, stateBattery_icons[0])

        self.stateConnect_label = QLabel('離線', self)
        self.stateConnect_label.setStyleSheet("QLabel { border: none; padding: 0;  margin: 0;background: transparent;}")
        self.stateConnect_label.setAlignment(Qt.AlignRight| Qt.AlignCenter)
        self.stateConnect_label.setFont(font)
        # setLabelIcon(self.stateConnect_label, )

        # 建立容器 widget 用來放置元件
        container_widget = QWidget(self)
        container_layout = QHBoxLayout(container_widget)
        container_layout.setContentsMargins(0, 0, 0, 0)

        container_layout1 = QHBoxLayout()
        container_layout2 = QHBoxLayout()
        container_layout3 = QHBoxLayout()

        # 將 QLabel 加入狀態列，並指定伸縮因子為1
        # 添加元件到容器
        container_layout1.addWidget(self.alarmNull_label)
        container_layout1.addWidget(self.alarm1_label)
        container_layout1.addWidget(self.alarm2_label)
        container_layout1.addItem(spacer)

        container_layout2.addItem(spacer_left)
        container_layout2.addWidget(self.datetime)
        container_layout2.addItem(spacer_right)

        container_layout3.addItem(spacer)
        container_layout3.addWidget(self.stateUSB_label)
        container_layout3.addWidget(self.stateBattery_label)
        container_layout3.addWidget(self.stateConnect_label)

        container_layout.addLayout(container_layout1)
        container_layout.addLayout(container_layout2)
        container_layout.addLayout(container_layout3)


        # status_bar.addWidget(self.alarmNull_label)
        # status_bar.addWidget(self.alarm1_label)
        # status_bar.addWidget(self.alarm2_label, 1)
        # status_bar.addWidget(self.datetime, 1)
        # status_bar.addWidget(self.state_label, 1)

        status_bar.addWidget(container_widget,1)
        #endregion


        # 創建中央主畫面及子畫面
        #region 主畫面
        main_frame = QFrame(self)
        main_frame.setGeometry(0, 40, 400, 360)
        # main_frame.setStyleSheet("background-color: lightblue;")
        main_frame.setStyleSheet("background-color: white;")  # 主畫面背景顏色

        # temperature_unit_default=unit_transfer.set_temperature_unit(unit=temperature_unit_text)
        # temperature=unit_transfer.convert_temperature(temperature=temperature,unit=temperature_unit_text)
        self.oxygen_label = QLabel("O<sub>2</sub>") # ° 為Alt 0176
        self.o2Data = QLabel(f"{self.oxygen_concentration:.2f}")
        self.o2Unite = QLabel("<strong>ppb</strong>")
        self.temperture_label=QLabel(f"T")
        self.tempData = QLabel(f"{self.temperature:.2f}")
        self.tempUnit = QLabel("<strong>°C</strong>")
        # self.oxygen_label.setAlignment(Qt.AlignCenter)  # 文字置中
        # self.temperture_label.setAlignment(Qt.AlignCenter)
        font.setPointSize(36)
        font2.setPointSize(16)
        font.setBold(True)
        self.oxygen_label.setFont(font)
        self.o2Data.setFont(font)
        self.o2Unite.setFont(font2)
        self.temperture_label.setFont(font)
        self.tempData.setFont(font)
        self.tempUnit.setFont(font2)
        font.setBold(False)
        main_frame_layout = QGridLayout(main_frame)
        main_frame_layout.setContentsMargins(75, 75, 75, 75)
        # main_frame_layout.setSpacing(0)  # 添加這一行以消除元素之間的間距
        main_frame_layout.addWidget(self.oxygen_label, 0, 0)
        main_frame_layout.addWidget(self.o2Data, 0, 1)
        main_frame_layout.addWidget(self.o2Unite, 0, 2)
        main_frame_layout.addWidget(self.temperture_label, 1, 0)
        main_frame_layout.addWidget(self.tempData, 1, 1)
        main_frame_layout.addWidget(self.tempUnit, 1, 2)

        #endregion

        #region 折線圖畫面
        # 創建折線圖畫面
        self.sub_frame = QFrame(self)
        self.sub_frame.setGeometry(400, 40, 400, 360)

        self.plot_canvas = plotCanvas(self, width=5, height=4)
        self.sub_frame.setStyleSheet("background-color: white;")  # 子畫面背景顏色
        # sub_label = QLabel('子畫面')
        # sub_label.setAlignment(Qt.AlignCenter)  # 文字置中
        # font.setPointSize(36)
        # sub_label.setFont(font)
        self.sub_frame_layout = QVBoxLayout(self.sub_frame)
        self.sub_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.sub_frame_layout.setSpacing(0)  # 添加這一行以消除元素之間的間距
        self.sub_frame_layout.addWidget(self.plot_canvas) # 在子畫面中加入 Matplotlib 的畫布
        # self.sub_frame_layout.addWidget(sub_label)

        #endregion

        
        # 創建功能列
        #region 功能列
        function_bar = QFrame(self)
        function_bar.setGeometry(0, 400, 800, 80)  # 設置功能列的尺寸
        function_bar.setStyleSheet("background-color: white;")  # 設置背景顏色

        # 在功能列中添加按鈕
        self.save_button = QPushButton(function_bar) # 資料儲存
        # test_button = QPushButton('測試', function_bar)
        # self.test_RTU_button = QPushButton('測試RTU', function_bar)
        self.quit_button=QPushButton('離開', function_bar) # 離開
        # self.lock_label = QLabel('螢幕鎖',function_bar)
        self.lock_button=QPushButton(function_bar) # 解鎖
        self.logout_button = QPushButton(function_bar) # 登出
        self.menu_button = QPushButton(function_bar) # 選單
        self.return_button = QPushButton(function_bar) # 返回



        # 設定按鈕大小
        button_width, button_height = 80, 80

        self.save_button.setFixedSize(button_width, button_height)
        # test_button.setFixedSize(button_width, button_height)
        # self.test_RTU_button.setFixedSize(button_width, button_height)
        self.quit_button.setFixedSize(button_width,button_height)
        # self.lock_label.setFixedSize(button_width, button_height)
        self.lock_button.setFixedSize(button_width, button_height)
        self.logout_button.setFixedSize(button_width, button_height)
        self.menu_button.setFixedSize(button_width, button_height)
        self.return_button.setFixedSize(button_width, button_height)
        
        font.setPointSize(14)
        self.save_button.setFont(font)
        # test_button.setFont(font)
        # self.test_RTU_button.setFont(font)
        self.quit_button.setFont(font)
        # self.lock_label.setFont(font)
        self.lock_button.setFont(font)
        self.logout_button.setFont(font)
        self.menu_button.setFont(font)
        self.return_button.setFont(font)

        # 按鈕圖示
        setButtonIcon(self.save_button, 'Save-icon.png')
        setButtonIcon(self.lock_button, lock_icons[0])
        setButtonIcon(self.logout_button, lock_icons[1])
        setButtonIcon(self.menu_button, 'Menu button.png')
        setButtonIcon(self.return_button, 'return icon.png')

        self.save_button.setStyleSheet('QPushButton { border: none; }')
        self.quit_button.setStyleSheet('QPushButton { border: none; }')
        self.lock_button.setStyleSheet('QPushButton { border: none; }')
        self.logout_button.setStyleSheet('QPushButton { border: none; }')
        self.menu_button.setStyleSheet('QPushButton { border: none; }')
        self.return_button.setStyleSheet('QPushButton { border: none; }')

        self.quit_button.clicked.connect(self.show_confirmation_dialog)
        # self.test_RTU_button.clicked.connect(self.conect_modbus_RTU)
        self.lock_button.clicked.connect(self.showLoginDialog)
        self.menu_button.clicked.connect(self.switch_to_menu)
        self.return_button.clicked.connect(self.switch_to_previous_page)
        self.logout_button.clicked.connect(self.logout_button_click)

        self.lock_button.setVisible(not self.isLogin)
        self.logout_button.setVisible(self.isLogin)
        self.menu_button.setVisible(True)
        self.return_button.setVisible(False)
        print('登入：',self.logout_button.isVisible())



        function_bar_layout = QHBoxLayout(function_bar)

        function_bar_layout1 = QHBoxLayout()
        function_bar_layout2 = QHBoxLayout()
        function_bar_layout3 = QHBoxLayout()

        function_bar_layout1.addWidget(self.save_button)
        # function_bar_layout1.addWidget(test_button)
        # function_bar_layout1.addWidget(self.test_RTU_button)
        function_bar_layout1.addWidget(self.quit_button)
        function_bar_layout1.addItem(spacer)

        function_bar_layout2.addItem(spacer_right)
        # function_bar_layout2.addWidget(self.lock_label)
        function_bar_layout2.addWidget(self.lock_button)
        function_bar_layout2.addWidget(self.logout_button)
        function_bar_layout2.addItem(spacer_left)
        
        function_bar_layout3.addItem(spacer)
        function_bar_layout3.addWidget(self.menu_button)
        function_bar_layout3.addWidget(self.return_button)

        function_bar_layout.addLayout(function_bar_layout1, 1)
        function_bar_layout.addLayout(function_bar_layout2, 1)
        function_bar_layout.addLayout(function_bar_layout3, 1)


        #endregion

        # 整體畫面配制
        #region 整體畫面
        # 創建一個放置元件的底層佈局
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        global_layout = QVBoxLayout(central_widget)
        global_layout.setContentsMargins(0, 0, 0, 0)  # 消除佈局的邊距
        global_layout.setSpacing(0)


        # 創建一個放置元件的子佈局
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.addWidget(main_frame, 1)  # 添加主畫面到佈局，第二個參數是優先級，表示佔用100的寬度
        main_layout.addWidget(self.sub_frame, 1) # 添加子畫面到佈局

        global_layout.addWidget(status_bar, 1)  # 添加狀態列到佈局佔用 1 的高度
        global_layout.addLayout(main_layout,8) # 添加子佈局到佈局
        global_layout.addWidget(function_bar, 2)  # 添加功能列到佈局，功能列佔用 2 的高度

        #endregion

        #主畫面堆疊
        #region 畫面堆疊
        # 在 MyWindow 類別的 __init__ 方法中初始化 QStackedWidget
        self.stacked_widget = QStackedWidget(self.sub_frame)
        print('Main Index:', self.stacked_widget.count()) #初始畫面頁數0
        self.plot_page_index = self.stacked_widget.addWidget(self.plot_canvas) # 此處僅添加 plot 畫面
        print('Plot Index:', self.stacked_widget.count()) #折線圖為第一頁
        self.stacked_widget.setCurrentIndex(self.plot_page_index) #設定初始顯示的畫面
        self.current_page_index = self.plot_page_index # 將當前的畫面索引設為 plot_page_index


        # 在 MyWindow 類別中添加 sub_pages 作為成員變數
        self.sub_pages = {}

        # 將QStackedWidget添加到sub_frame佈局
        self.sub_frame_layout.addWidget(self.stacked_widget)

        #endregion

        #region 每秒動態更新（日期時間、警告、圖表及讀取modbus數據）    
        # self.timer = QTimer(self) # 更新日期時間的 QTimer
        # PPV.timer.timeout.connect(self.update_modbus_data)
        PPV.timer.timeout.connect(self.update)
        PPV.timer.start(1000)  # 每秒更新一次



        # 更新一次日期時間，避免一開始顯示空白
        # self.update()
        #endregion


        # 顯示視窗
        self.show()

    #endregion
        
    #region testClicked    
    def testClicked(self):
        print('測試按鈕')
    #endregion
   
            
    #region 動態更新
    def update(self):
        # global oxygen_concentration, temperature
        try:
            #region modbus RTU讀取
            # 定義一個函數，用於在執行緒中執行Modbus讀取
            def modbus_read_thread():
                # global oxygen_concentration, temperature

                # 讀取SQL的暫存資料表
                self.sqlGasUnit = int(PySQL.selectSQL_Reg(regDF = 4, regKey = 4))
                self.sqlDateFormat = int(PySQL.selectSQL_Reg(regDF = 4, regKey = 1))
                self.sqlTempUnit = int(PySQL.selectSQL_Reg(regDF = 4, regKey = 0))
                
                #region 讀取modbus數據
                try:
                    # 成功連線下，以下讀取modbus可以執行
                    #region 讀取R1X（只要讀bit就好）
                    r1x = PPV.instrument_ID1.read_bits(0, 2, functioncode=1)

                    cache_R1X={}
                    for address, value in enumerate(r1x):
                        cache_R1X[address] = value

                    for address, value in cache_R1X.items():
                        if value != int(PySQL.selectSQL_Reg(regDF=1, regKey=address)): # modbus值與暫存SQL不一致，將暫存SQL寫入modbus
                            # PySQL.updateSQL_Reg(1, address, value)
                            PPV.instrument_ID1.write_bit(address, int(PySQL.selectSQL_Reg(regDF=1, regKey=address)))
                    #endregion

                    #region 讀取R3X
                    # 讀取濃度、溫度變動值
                    self.oxygen_concentration = PPV.instrument_ID3.read_float(PPV.R3X_address('Gas'), functioncode=4)
                    self.temperature = PPV.instrument_ID3.read_float(PPV.R3X_address('Temperature'), functioncode=4)

                    # 讀取modbus的Reg設定值
                    # modbusGasUnit = PPV.instrument_ID1.read_register(PPV.R4X_address('Set Gas Unit'), functioncode=3)
                    # modbusDateFormat =PPV.instrument_ID1.read_register(PPV.R4X_address('Date Formate'), functioncode=3)
                    # modbusTempUnit = PPV.instrument_ID1.read_register(PPV.R4X_address('Temp unit'), functioncode=3)

                    #endregion

                    #region 讀取R4X
                    # 讀取地址範圍為 0 到 15 的保持寄存器值
                    values_0_to_15 = PPV.instrument_ID1.read_registers(0, 15, functioncode=3)

                    # 讀取地址範圍為 16 的浮點數值
                    value_16 = PPV.instrument_ID1.read_float(16, functioncode=3)

                    # 讀取地址範圍為 18 到 26 的保持寄存器值
                    values_18_to_26 = PPV.instrument_ID1.read_registers(18, 8, functioncode=3)

                    # 將讀取的保持寄存器值合併為一個字典
                    cache_R4X = {}
                    for address, value in enumerate(values_0_to_15):
                        cache_R4X[address] = value

                    # 將地址 16 加入字典並視為浮點數
                    cache_R4X[16] = value_16

                    for address, value in enumerate(values_18_to_26, start=18):
                        cache_R4X[address] = value

                    # 將讀取的保持寄存器值與暫存資料表進行比對
                    for key, value in cache_R4X.items():
                        # 由於離線時有更動暫存資料表，恢復連線後與modbus比對數值不一致，則將暫存資料表的值寫進modbus
                        if key == 16:
                            if PPV.instrument_ID1.read_float(key, functioncode=3) != float(PySQL.selectSQL_Reg(regDF=4, regKey=key)):
                                PPV.instrument_ID1.write_float(key, float(PySQL.selectSQL_Reg(regDF=4, regKey=key)), functioncode=6)
                        else:
                            if value != int(PySQL.selectSQL_Reg(regDF=4, regKey=key)):
                                PPV.instrument_ID1.write_register(key, int(PySQL.selectSQL_Reg(regDF=4, regKey=key)), functioncode=6)
                    #endregion

                    self.stateConnect_label.setText('已連線')
                    # print(f'O2:{oxygen_concentration:.2f} {o2_GasUnitDist[setGasUnit]}, T:{temperature:.2f} {tempUnitDist[temp_unit]}')


                except minimalmodbus.NoResponseError as e:
                    # 出現離線狀態直接執行此區塊

                    self.stateConnect_label.setText('離線')
                    # print(f'No response from the instrument: {e}')
                except AttributeError as e: # 略過無法取得裝置變數的錯誤（因沒有埠號）
                    pass
                except serial.SerialException as e: # 略過未使用埠號、虛擬埠的錯誤
                    pass
                except Exception as e:
                    traceback.print_exc()
                    print(f'Thread Inside Exception: {e}')
                #endregion

            # 執行緒啟動與modbus互動
            modbus_thread = threading.Thread(target=modbus_read_thread)
            modbus_thread.start()
            #endregion

            #region 警告圖示動態顯示
            self.alarm1_label.setVisible(PPV.alarm(PySQL.selectAlarmRelay(), self.temperature, self.oxygen_concentration))
            if self.alarm1_label.isVisible():
                self.alarmNull_label.setVisible(False)

            #endregion
            
            #region 時間動態顯示
            current_datetime = QDateTime.currentDateTime()
            formatted_datetime = current_datetime.toString(f"{PPV.dateFormat[self.sqlDateFormat][1]} hh:mm:ss")
            PPV.current_datetime = current_datetime
            self.datetime.setText(formatted_datetime)

            #endregion

            #region 氧氣濃度、溫度動態顯示
            self.o2Data.setText(f"{self.oxygen_concentration:.2f}")
            self.o2Unite.setText(f"<strong>{PPV.o2_GasUnitDist[self.sqlGasUnit]}</strong>")
                    
            self.tempData.setText(f"{self.temperature:.2f}")
            self.tempUnit.setText(f"<strong>{PPV.tempUnitDist[self.sqlTempUnit]}</strong>")

            # self.label.setText(f'Modbus Value: {round(value_read_float, 2)}')
            # print(f'O2:{oxygen_concentration:.2f}, T:{temperature:.2f} {temperature_unit_default}')
            #endregion
            
            
            #region 更新圖表
                
            # 清除之前的圖例
            self.plot_canvas.ax.clear()

            PPV.plotTime = PPV.plotTimeDict[int(PySQL.selectSQL_Var('plotTime'))]
            # 重新繪製折線圖
            self.plot_canvas.plot(temperature_unit = temperature_unit_text, 
                                oxygen_concentration = self.oxygen_concentration, 
                                temperature = self.temperature #temperature: Celsius, Fahrenheit
                                )  

            # 在這裡更新畫布
            self.plot_canvas.draw()
            #endregion

        except Exception as e:
            traceback.print_exc()
            print(f'Exception in update_datetime: {e}')


    #endregion

    #region 關閉程式警告視窗
    def show_confirmation_dialog(self):
        # 顯示確認對話框
        reply = QMessageBox.question(self, '程式關閉', '確定要關閉程式嗎？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # 如果用戶選擇 "Yes"，則關閉應用程式
            # response.close()
            PPV.stop_flask_api() # 程式關閉時關閉Flask API
            QApplication.quit()

    #endregion

    #region 登入視窗
    def showLoginDialog(self):

        # 顯示帳號和密碼輸入對話框
        login_dialog = LoginDialog()
        result = login_dialog.exec_()

        if result == LoginDialog.Accepted: # 使用者按下確定按鈕，取得輸入的值
            self.isLogin=True
            # username = login_dialog.username_input.text()
            # password = login_dialog.password_input.text()
            self.logout_button.setVisible(self.isLogin)
            self.lock_button.setVisible(not self.isLogin)
            # print('logout_button:',self.logout_button.isVisible())
            print('登入成功')
            PPV.presentUser = login_dialog.get_global_loginUser()

            print('main.py:',PPV.presentUser.userInfo())

        else:
            print('登入取消')


    #endregion



    #region 登入成功行為
    def handle_login_success(self, checkLogin):
        # 登入成功時觸發，將 logout_button 由不可見改為可見
        print('收到 login_successful 信號:', checkLogin)
        self.logout_button.setVisible(True)
    #endregion
    
    #region 登出行為
    def logout_button_click(self):
        # 顯示確認對話框
        reply = QMessageBox.question(self, '登出', '確定要登出嗎？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # 如果用戶選擇 "Yes"，則登出應用程式
                    
            self.isLogin=False

            QMessageBox.information(self, '登出成功', '返回主頁面')
            self.logout_button.setVisible(self.isLogin) 
            print('logout_button_click:',self.logout_button.isVisible())

            # 將畫面切換回主畫面（清空堆疊）
            # 判斷是否只剩下一頁，如果是，則不執行刪除
            print('Totle Pages:', self.stacked_widget.count())
            if self.stacked_widget.count() > 1:
                print('Remove Pages:', self.stacked_widget.count()-1)
                
                while self.stacked_widget.count() > 1:
                    widget = self.stacked_widget.widget(self.stacked_widget.count() - 1)  # 取得最頂層的頁面
                    print('Remaining Pages:', self.stacked_widget.count())
                    if widget:
                        self.stacked_widget.removeWidget(widget)
                        widget.deleteLater()
                # print('Back to First Pages:', self.stacked_widget.count())
                        
                self.sub_pages={}
                
            else:
                print(f'主畫面登出（{self.stacked_widget.count()}）')
            
            self.stacked_widget.setCurrentIndex(self.plot_page_index)
            self.current_page_index = self.plot_page_index
            
            # print('Plot Index:', self.plot_page_index)
            print('Plot Index:',self.stacked_widget.count())

            self.lock_button.setVisible(not self.isLogin)
            self.return_button.setVisible(False)
            self.menu_button.setVisible(True)
        else:
            return
        
    #endregion
        

    #region 連接COM Port視窗並讀取氧氣濃度及溫度
    # def connect_modbus_RTU(self):
    #     connectGUI=ModbusRTUConfigurator(self)
    #     connectGUI.value_updated.connect(self.set_main_values)
    #     self.data_updated.connect(self.update_main_label)
    #     connectGUI.exec_()

    # @pyqtSlot(float)
    # def update_main_label(self, temperature):
    #     self.oxygen_label.setText(f'O₂: {oxygen_concentration:.2f} ppb, T: {temperature:.2f} °C')

    # def set_main_values(self, temperature):
    #     # 設定 oxygen_concentration 和 temperature 的值
    #     # oxygen_concentration = round(oxygen, 2)
    #     temperature = round(temperature, 2)
    #     # 發送 oxygen_concentration 和 temperature 更新的信號
    #     self.data_updated.emit(temperature)
    
    #endregion


    # 在MyWindow類別中新增一個方法用於由主畫面切換主選單
    #region 前往主選單（第二頁）
    def switch_to_menu(self):
        if self.isLogin == False:
            print('請先登入解鎖')
            self.is_login_dialog()
            
        else:
            print('進入目錄成功')
            self.menu_page_index = self.stacked_widget.addWidget(self.create_menu_page()) #此處添加了目錄畫面（第二頁）
            if self.menu_page_index is None:
                self.menu_page = self.create_menu_page()
                self.menu_page_index = self.stacked_widget.addWidget(self.menu_page)

            if self.current_page_index != self.menu_page_index:
                self.stacked_widget.setCurrentIndex(self.menu_page_index)
                self.current_page_index = self.menu_page_index

            else:
                # 如果當前已經是主選單索引，再次切換到主選單
                self.stacked_widget.setCurrentIndex(self.menu_page_index)

            # 根據當前的畫面索引顯示或隱藏按鈕
            self.menu_button.setVisible(self.current_page_index == self.plot_page_index)
            # self.test_RTU_button.setVisible(self.current_page_index == self.plot_page_index)
            self.return_button.setVisible(self.current_page_index == self.menu_page_index)

            print('主選單 Index:', self.stacked_widget.count())

    #endregion
    
    # 創建主選單畫面
    #region 建立主選單及其元件、配制
    def create_menu_page(self):       

        menu_page = QFrame(self)
        menu_page.setStyleSheet("background-color: white;")  # 選單畫面背景顏色

        font.setPointSize(16)
        # menu_label = QLabel('選單')
        # menu_label.setAlignment(Qt.AlignCenter)  # 文字置中
        # menu_label.setFont(font)
        menu_page_layout = QGridLayout(menu_page)
        menu_page_layout.setSpacing(0)
        # menu_page_layout.addWidget(menu_label)

        # 顯示四個按鈕
        self.set_button = QPushButton(menu_page) # 設定
        self.calibrate_button = QPushButton( menu_page) # 校正
        self.record_button = QPushButton(menu_page) # 記錄
        self.identify_button = QPushButton(menu_page) # 識別

            # 設定按鈕大小
        button_width, button_height = 125, 125

        self.set_button.setFixedSize(button_width, button_height)
        self.calibrate_button.setFixedSize(button_width, button_height)
        self.record_button.setFixedSize(button_width, button_height)
        self.identify_button.setFixedSize(button_width, button_height)

        # 設定按鈕的背景顏色，方便檢查它們的可見性
        # self.set_button.setStyleSheet("background-color: white;")
        # self.calibrate_button.setStyleSheet("background-color: white;")
        # self.record_button.setStyleSheet("background-color: white;")
        # self.identify_button.setStyleSheet("background-color: white;")


        setButtonIcon(self.set_button, stateInbMenu_icons[1], text = "設\n定") # text='設定'
        setButtonIcon(self.calibrate_button, stateInbMenu_icons[2], text = "校\n正") # text='校正'
        setButtonIcon(self.record_button, stateInbMenu_icons[3], text = "記\n錄") # text='記錄'
        setButtonIcon(self.identify_button, stateInbMenu_icons[4], text = "識\n別") # text='識別'

        self.set_button.setStyleSheet('QPushButton { border: none;}')
        self.calibrate_button.setStyleSheet('QPushButton { border: none;}')
        self.record_button.setStyleSheet('QPushButton { border: none;}')
        self.identify_button.setStyleSheet('QPushButton { border: none;}')


        # paintEvent(self.set_button, None)
        # paintEvent(self.calibrate_button, None)
        # paintEvent(self.record_button, None)
        # paintEvent(self.identify_button, None)

        self.set_button.setFont(font)
        self.calibrate_button.setFont(font)
        self.record_button.setFont(font)
        self.identify_button.setFont(font)

        # 連接按鈕點擊事件（前往各個子選單）
        self.set_button.clicked.connect(lambda: self.sub_menu_page("設定",self.set_button.styleSheet()))
        self.calibrate_button.clicked.connect(lambda: self.sub_menu_page("校正",self.calibrate_button.styleSheet()))
        self.record_button.clicked.connect(lambda: self.sub_menu_page("記錄",self.record_button.styleSheet()))
        self.identify_button.clicked.connect(lambda: self.sub_menu_page("識別",self.identify_button.styleSheet()))

        # 將按鈕添加到GridLayout中
        menu_page_layout.addWidget(self.set_button, 0, 0, 1, 1)
        menu_page_layout.addWidget(self.calibrate_button, 0, 1, 1, 1)
        menu_page_layout.addWidget(self.record_button, 1, 0, 1, 1)
        menu_page_layout.addWidget(self.identify_button, 1, 1, 1, 1)

        # print('登入：',self.logout_button.isVisible())
        return menu_page
    
    #endregion

    # 主選單前往子選單畫面
    #region 在主選單中前往下一個子選單清單頁面（第三頁）
    def sub_menu_page(self, page_name, _style):
        print('登入：',self.logout_button.isVisible())
        print('進入：', page_name)

        # 隱藏選單按鈕
        self.menu_button.setVisible(False)

        # 判斷是否已經創建了該子畫面
        if page_name not in self.sub_pages or not self.stacked_widget.widget(self.sub_pages[page_name]):
            # 如果還沒有，則創建一個新的子畫面
            self.subMenu_page = subMenuFrame(page_name, _style, self.sub_pages, self.stacked_widget)

            # 添加到堆疊中
            sub_page_index = self.stacked_widget.addWidget(self.subMenu_page)
            self.sub_pages[page_name] = sub_page_index
        else:
            # 如果已經存在，取得子畫面的索引
            sub_page_index = self.sub_pages[page_name]

            # 強制刷新子畫面
            self.menuSub_page = self.stacked_widget.widget(sub_page_index)
            # menuSub_page.update()  # 假設您的子畫面有 update 方法

        # # 設定當前顯示的子畫面索引
        self.stacked_widget.setCurrentIndex(sub_page_index)
        self.current_page_index = sub_page_index

        print(f'{page_name} Index: {self.stacked_widget.count()}')

        # 顯示返回按鈕
        self.return_button.setVisible(True)

    #endregion

    #region 是否有登入
    def is_login_dialog(self):
        # 顯示確認對話框
        message_text="你要先登入解鎖才能進入選單"
        QMessageBox.critical(self, '請先登入', message_text)
        print('選單不可用')

    #endregion


    # 在 MyWindow 中新增一個方法用於返回上一個畫面
    #region 返回
    def switch_to_previous_page(self):

        if self.stacked_widget is not None:
        
            # 如果當前是選單畫面，直接返回主畫面
            if self.current_page_index == self.menu_page_index:
                self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())
                self.current_page_index = self.plot_page_index
        
            else:
                # 清除之前的子畫面
                previous_sub_frame = self.stacked_widget.currentWidget()
                self.stacked_widget.removeWidget(previous_sub_frame)

                # 更新當前的畫面索引
                self.current_page_index = self.stacked_widget.currentIndex()

                # 如果返回主畫面，將menu_page_index設為None
                if self.current_page_index == self.plot_page_index:
                    self.menu_page_index = None

                # 切換到更新後的畫面索引
                self.stacked_widget.setCurrentIndex(self.current_page_index)

            # 刪除已經移除的子畫面的索引
            for title, sub_page_index in list(self.sub_pages.items()):
                if sub_page_index not in range(self.stacked_widget.count()):
                    del self.sub_pages[title]

            # 根據當前的畫面索引顯示或隱藏按鈕
            self.menu_button.setVisible(self.current_page_index == self.plot_page_index)
            self.return_button.setVisible(self.current_page_index != self.plot_page_index)

        print('Last Index:', self.stacked_widget.count())

    #endregion 

    def closeEvent(self, event):
        PPV.stop_flask_api() # 程式關閉時關閉Flask API
        event.accept()

#endregion


if __name__ == '__main__':


    print("Current working directory:", os.getcwd())

    try:
        app = QApplication(sys.argv)
        window = MyWindow()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        input("Press Enter to exit")
        # 等待使用者按 Enter 鍵


    # app = QApplication(sys.argv)
    # window = MyWindow()
    # sys.exit(app.exec_())

        