#zh-tw

# mainWithUI.py
# 以UI / XML檔案生成圖形化介面

# 此程式碼為主畫面，顯示折線圖為主
# 由於介面往上堆疊，排除初始化介面，折線圖為第一層，進入主選單為第二層，主選單後進入各個子選單為第三層
    # 介面順序由下而上疊：self.plot_canvas/self.menu_page/self.menuSub_page

# 16777215
# import picture.icon.icon_rc


try:
    
    import sys, os, traceback, minimalmodbus, threading, platform, serial
    # sys.path.append("venv-py3_9/Lib/site-packages")
    # print(sys.path)

    

    from PyQt5.QtWidgets import \
        QApplication, QMainWindow, QWidget, QStatusBar, QVBoxLayout,\
        QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QFrame, QGridLayout,\
        QPushButton, QStackedWidget, QMessageBox, QDesktopWidget\
        
    from ui.SentrakGUI_ui import Ui_MainWindow as SentrakGUI_MainWindow
    from ui.manu_page_ui import Ui_menu_page as menu_page

    # import pyqtgraph as pg
        
    from PyQt5.QtCore import Qt, QDateTime
    from PyQt5.QtGui import QFont
    from imgResource import setButtonIcon, setLabelIcon, \
        stateAlarm_icons, stateWire_icons, stateRecord_icons\
        ,stateBatteryCharge_icons ,stateBattery_icons ,stateInbMenu_icons, lock_icons

    # from modbus_RTU_Connect_GUI import ModbusRTUConfigurator
    import ProjectPublicVariable as PPV
    import PySQL

    from unit_transfer import unit_transfer
    # from plotCanvasMatplot import plotCanvasMatplot #圖表內部配制
    from plotCanvasPG import PlotCanvasPG
    from subMenuFrame import subMenuFrame #子選單內部配制
    # from img_to_base64 import image_to_base64
    from login import LoginDialog

    from functools import lru_cache,cache


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

# spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
# spacer_right = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
# spacer_left = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)


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
class MyWindow(QMainWindow, SentrakGUI_MainWindow):
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
        self.setupUi(self)

        # PPV.start_flask_api() # 啟動Flask API
        # 設定視窗標題
        # self.setWindowTitle("Sentrak_RaspPie_GUI")

        self.isLogin=False

        self.oxygen_concentration = 0.00 # 16712.32767
        self.temperature = 0.00 # 16774.26214


        self.sqlTempUnit = 0
        self.sqlDateFormat = 2

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

        self.initUI()

        #endregion

    def initUI(self):
        
        font.setPointSize(14)

        
        self.plot_canvas = PlotCanvasPG(self) # 使用pyqtgraph
        

        self.quitBtn.clicked.connect(self.show_confirmation_dialog)
        self.lockBtn.clicked.connect(self.showLoginDialog)
        self.menuBtn.clicked.connect(self.switch_to_menu)
        self.returnBtn.clicked.connect(self.switch_to_previous_page)
        self.logoutBtn.clicked.connect(self.logout_button_click)

        self.lockBtn.setVisible(not self.isLogin)
        self.logoutBtn.setVisible(self.isLogin)
        self.menuBtn.setVisible(True)
        self.returnBtn.setVisible(False)
        print('登入：',self.logoutBtn.isVisible())



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

                #region 時間動態顯示
                current_datetime = QDateTime.currentDateTime()
                formatted_datetime = current_datetime.toString(f"{PPV.dateFormat[self.sqlDateFormat][1]} hh:mm:ss")
                PPV.current_datetime = current_datetime
                self.datetime.setText(formatted_datetime)

                #endregion

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
                    self.oxygen_concentration = round(PPV.instrument_ID3.read_float(PPV.R3X_address('Gas'), functioncode=4),2)

                    self.temperature = round(PPV.instrument_ID3.read_float(PPV.R3X_address('Temperature'), functioncode=4),2)

                    caliGasPercent = round(PPV.instrument_ID3.read_float(PPV.R3X_address('Calibration Gas %'), functioncode=4),2)

                    caliT = round(PPV.instrument_ID3.read_float(PPV.R3X_address('Calibration T'), functioncode=4),2)

                    caliCT1 = round(PPV.instrument_ID3.read_float(PPV.R3X_address('Calibration CT1'), functioncode=4),2)

                    caliCT2 = round(PPV.instrument_ID3.read_float(PPV.R3X_address('Calibration CT2'), functioncode=4),2)

                    readV3_volt = round(PPV.instrument_ID3.read_float(PPV.R3X_address('Read V3 voltage'), functioncode=4),2)

                    readV2_volt = round(PPV.instrument_ID3.read_float(PPV.R3X_address('Read V2 voltage'), functioncode=4),2)

                    r3x_Value16To20=PPV.instrument_ID3.read_registers(16,5, functioncode=4)

                    

                    # 每秒R3X記錄測試1
                    # r3xRecord=PPV.instrument_ID3.read_registers(0,21, functioncode=4)
                    # r3xRecord.insert(0,formatted_datetime)
                    # r3xRecordTuple=tuple(r3xRecord)
                    # PySQL.insertSQL_R3X_Record_Test1(r3xRecordTuple)
                    # print(r3xRecordTuple)

                    # 每秒R3X記錄測試2
                    
                    # r3xRecord=[formatted_datetime, self.oxygen_concentration, self.temperature, caliGasPercent, caliT, caliCT1, caliCT2, readV3_volt, readV2_volt]
                    # r3xRecord.extend(r3x_Value16To20)
                    # r3xRecordTuple=tuple(r3xRecord)
                    # PySQL.insertSQL_R3X_Record_Test2(r3xRecordTuple)
                    
                    # print(r3xRecordTuple)

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
            

            #region 氧氣濃度、溫度動態顯示
            self.o2Data.setText(f"{self.oxygen_concentration:.2f}")
            self.o2Unite.setText(f"<strong>{PPV.o2_GasUnitDist[self.sqlGasUnit]}</strong>")
                    
            self.tempData.setText(f"{self.temperature:.2f}")
            self.tempUnit.setText(f"<strong>{PPV.tempUnitDist[self.sqlTempUnit]}</strong>")

            # self.label.setText(f'Modbus Value: {round(value_read_float, 2)}')
            # print(f'O2:{oxygen_concentration:.2f}, T:{temperature:.2f} {temperature_unit_default}')
            #endregion
            
            self.updatePlot()
            

        except Exception as e:
            traceback.print_exc()
            print(f'Exception in update_datetime: {e}')

    #region 更新圖表
    # @lru_cache()
    def updatePlot(self):
                
        # 清除之前的圖例
        # self.plot_canvas.ax.clear() # PG不使用

        PPV.plotTime = PPV.plotTimeDict[int(PySQL.selectSQL_Var('plotTime'))]
        # 重新繪製折線圖
        self.plot_canvas.plot(temperature_unit = temperature_unit_text, 
                            oxygen_concentration = self.oxygen_concentration, 
                            temperature = self.temperature #temperature: Celsius, Fahrenheit
                            )  

        # 在這裡更新畫布
        # self.plot_canvas.draw() # PG不使用
    #endregion


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


    #region 登入、登出行為
    #region 登入視窗
    def showLoginDialog(self):

        # 顯示帳號和密碼輸入對話框
        login_dialog = LoginDialog()
        result = login_dialog.exec_()

        if result == LoginDialog.Accepted: # 使用者按下確定按鈕，取得輸入的值
            self.isLogin=True
            # username = login_dialog.username_input.text()
            # password = login_dialog.password_input.text()
            self.logoutBtn.setVisible(self.isLogin)
            self.lockBtn.setVisible(not self.isLogin)
            # print('logoutBtn:',self.logoutBtn.isVisible())
            print('登入成功')
            PPV.presentUser = login_dialog.get_global_loginUser()

            print('main.py:',PPV.presentUser.userInfo())

        else:
            print('登入取消')


    #endregion



    #region 登入成功行為
    def handle_login_success(self, checkLogin):
        print('收到 login_successful 信號:', checkLogin)
        self.logoutBtn.setVisible(True)
    #endregion

    #region 是否有登入
    def is_login_dialog(self):
        # 顯示確認對話框
        message_text="你要先登入解鎖才能進入選單"
        QMessageBox.critical(self, '請先登入', message_text)
        print('選單不可用')

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
            self.logoutBtn.setVisible(self.isLogin) 
            print('logoutBTN_click:',self.logoutBtn.isVisible())

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

            self.logoutBtn.setVisible(not self.isLogin)
            self.returnBtn.setVisible(False)
            self.menuBtn.setVisible(True)
        else:
            return
        
    #endregion

    #endregion
        

    #region 前往主選單行為
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
            self.menuBtn.setVisible(self.current_page_index == self.plot_page_index)
            self.returnBtn.setVisible(self.current_page_index == self.menu_page_index)

            print('主選單 Index:', self.stacked_widget.count())

    #endregion
    
    # 創建主選單畫面
    #region 建立主選單及其元件、配制
    def create_menu_page(self): 
        menuFrame=QFrame()

        menu = menu_page()
        menu.setupUi(menuFrame)

        menu.set_button.clicked.connect(lambda: self.sub_menu_page("設定",menu.set_button.styleSheet()))
        menu.calibrate_button.clicked.connect(lambda: self.sub_menu_page("校正",menu.calibrate_button.styleSheet()))
        menu.record_button.clicked.connect(lambda: self.sub_menu_page("記錄",menu.record_button.styleSheet()))
        menu.identify_button.clicked.connect(lambda: self.sub_menu_page("識別",menu.identify_button.styleSheet()))


        # print('登入：',self.logoutBtn.isVisible())
        return menuFrame
    
    #endregion

    # 主選單前往子選單畫面
    #region 在主選單中前往下一個子選單清單頁面（第三頁）
    def sub_menu_page(self, page_name, _style):
        print('登入：',self.logoutBtn.isVisible())
        print('進入：', page_name)

        # 隱藏選單按鈕
        self.menuBtn.setVisible(False)

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
        self.returnBtn.setVisible(True)

    #endregion
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
            self.menuBtn.setVisible(self.current_page_index == self.plot_page_index)
            self.returnBtn.setVisible(self.current_page_index != self.plot_page_index)

        print('Last Index:', self.stacked_widget.count())

    #endregion 

    #region Docker的Flask與程式連動
    def closeEvent(self, event):
        PPV.stop_flask_api() # 程式關閉時關閉Flask API
        event.accept()

    #endregion

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

        