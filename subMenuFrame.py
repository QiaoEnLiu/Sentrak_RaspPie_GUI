#zh-tw

# menuSubFrame.py
# 此程式碼為子選單畫面（第三層）：當main.py的功能選單的四個按鈕（設定、校正、記錄、識別）偵測到點擊事件時，所執行的程式碼並將子畫面刷新為清單畫面
    # 各別進入的子選單清單畫面為底下第四層

    # 設定
        # 顯示、警報輸出、類比輸出、感測器溫度保護、診斷、通訊、時間、語言

    # 校正
        # 感測器校正、大氣壓力校正、類比輸出校正

    # 記錄
        # 觀看記錄、統計表、下載記錄至隨身碟、記錄方式設定

    # 識別
        # 登入身份、儀器資訊、感測器資訊
# 可參考ProjectPublicVariable的subMenu字典

try:
    import sys
    sys.path.append("venv-py3_9/Lib/site-packages")
    
    import os, traceback

    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget,\
        QListWidgetItem, QHBoxLayout
    from PyQt5.QtCore import Qt, QByteArray
    from PyQt5.QtGui import QFont, QPixmap, QImage
    
    import ProjectPublicVariable as PPV

    # 設定 >>
    from setDisplayOption import displayOptionFrame # 「顯示」
    from setAlarmRelayMenu import setAlarmRelayMenuFrame # 「警報輸出」選項介面
    from setAnalogyOutputOption import analogyOutputOptionFrame # 「類比輸出」選項介面
    from setSensorTempLimit import setSensorTempLimitFrame # 「感測器溫度保護」介面

    from setCommunicationOption import comOptionFrame # 「通訊」選項介面


    from setTime import setTimeFrame # 「時間」選項介面

    # 校正 >>
    from calibrateAnalogyOutput import calibrateAnalogyOutputFrame # 「類比輸出校正」介面

    # 記錄 >>
    from recordDownloadFile import recordDownloadFileFrame # 「下載記錄至隨身碟」介面


    # 識別 >>
    from id_Frame import id_LogIn_Frame # 登入訊息
    from id_deviceInfo import deviceInfoFrame # 「儀器資訊」介面

    # 未實作功能測試介面
    from testEndFrame import testEndFrame

    
    from imgResource import setLabelIcon
    from img_to_base64 import image_to_base64

except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()
itemTitleSize = QFont()
itemTitleSize.setPointSize(20)
itemdescribeSize = QFont()
itemdescribeSize.setPointSize(14)
class subMenuFrame(QWidget):

    #region 清單畫面
    def __init__(self, title, _style, sub_pages, stacked_widget):
        super().__init__()
        self.sub_pages = sub_pages
        self.stacked_widget = stacked_widget
        self.id_login_frame = id_LogIn_Frame

        self.title = title
        # print(title,PPV.presentUser.userInfo())

        # 標題列
        #region 標題列
        title_layout = QVBoxLayout()        
        self.title_label = QLabel(self.title, self)
        # title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(20)
        self.title_label.setFont(font)
        # self.title_label.setStyleSheet(_style)
        title_layout.addWidget(self.title_label)
        #endregion

        # 清單
        #region 清單元件配制
        content_layout = QVBoxLayout()
        # content_layout.setContentsMargins(0, 0, 0, 0)
        # content_layout.setSpacing(0)

        # 內容使用QListWidget
        self.list_widget = QListWidget(self)

        # 依功能添加列各自表項
        if self.title in PPV.subMenu:
            for option in PPV.subMenu[self.title].keys():
                self.create_list_item(option)
                self.itemDescribe(PPV.subMenu.get(self.title, {}).get(option, None))
        #region 非模組化寫法
        # if self.title == '設定':
        #     for option in ['顯示', '警報輸出', '類比輸出', '感測器溫度保護', '診斷', '通訊', '時間', '語言']:
        #         self.create_list_item(option)
        #         self.itemDescribe(option)

        # elif self.title == '校正':
        #     for option in ['感測器校正', '大氣壓力校正', '類比輸出校正']:
        #         self.create_list_item(option)
        #         self.itemDescribe(option)

        # elif self.title == '記錄':
        #     for option in ['觀看記錄', '統計表', '下載記錄至隨身碟', '記錄方式設定']:
        #         self.create_list_item(option)
        #         self.itemDescribe(option)

        # elif self.title == '識別':
        #     for option in ['登入身份', '儀器資訊', '感測器資訊']:
        #         self.create_list_item(option)
        #         self.itemDescribe(option)
                
        #endregion

        # 將垂直滾動條設置為不可見
        # self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        content_layout.addWidget(self.list_widget)
        #endregion

        # print(f'{self.title} Index: {self.stacked_widget.count()} （menySubFrame.py）')

        # 整體佈局
        #region 標題列及清單配制
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addLayout(title_layout)
        main_layout.addLayout(content_layout)
        #endregion

    #endregion
        
    #region 清單內容
    def create_list_item(self, option):

        # 創建 QListWidgetItem
        item = QListWidgetItem()
        
        # 設置清單圖示及其內部配制
        #region 清單圖示
        list_icon = QLabel('圖示')
        list_icon.setStyleSheet("border: 2.5px solid black;border-right: 0px;")

        setLabelIcon(list_icon,'test_icon.png')
        
        # pixmap = QPixmap('picture/icon/test_icon.png')  # 請替換為您的實際圖示路徑
        # list_icon_path = os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")), "picture/icon", "test_icon.png")
        # icon_base64 = image_to_base64(list_icon_path)
        # icon_bytes = QByteArray.fromBase64(icon_base64.encode())
        # list_icon.setPixmap(QPixmap.fromImage(QImage.fromData(icon_bytes)).scaled(72, 72))
        # print('icon Hright1:', list_icon.pixmap().height())
        # print('icon Hright2:', pixmap.scaledToHeight(72).height())

        # label_font = list_icon.font()  # 獲取 QLabel 的字型
        # font_size = label_font.pointSize()  # 獲取字型大小
        # print('icon Hright Font:', font_size)
         
        # list_icon.setPixmap(pixmap.scaled(72, 72))  # 調整大小以符合您的需求
        item_label = QLabel(option)# 設置文字
        self.describe_label = QLabel()

        # font.setPointSize(pixmap.scaledToHeight(72).height()*30//80)
        # font.setPointSize(20)
        item_label.setFont(itemTitleSize)
        item_label.setStyleSheet("border: 2.5px solid black;border-bottom: 0px;")
        item_label.setContentsMargins(0, 0, 0, 0)
        # print('item_label:', item_label.font().pointSize())

        #endregion

        # 設置清單描述配制
        #region 清單描述及其配制

        self.describe_label.setText('描述')
        # font.setPointSize(pixmap.scaledToHeight(72).height()*15//80)
        # font.setPointSize(6)
        self.describe_label.setFont(itemdescribeSize)
        self.describe_label.setStyleSheet("border: 2.5px solid black;border-top: 0px; color: gray")
        self.describe_label.setContentsMargins(0, 0, 0, 0)
        # print('self.describe_label:', self.describe_label.font().pointSize())
        
        #endregion

        #region清單配製
        # 將圖示和文字排列在一行
        item_layout = QHBoxLayout()
        icon_layout = QHBoxLayout()
        label_layout = QVBoxLayout()
        item_label_layout = QHBoxLayout()
        describe_layout = QHBoxLayout()

        item_layout.setSizeConstraint(QHBoxLayout.SetMinAndMaxSize)
        icon_layout.setSizeConstraint(QHBoxLayout.SetMinAndMaxSize)
        label_layout.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)
        item_label_layout.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)
        describe_layout.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)

        # item_layout.addWidget(item_frame)
        # 將圖示和文字排列在一行，並確保沒有額外空間
        item_layout.setSpacing(0)
        icon_layout.addWidget(list_icon)

        label_layout.addLayout(item_label_layout)
        label_layout.addLayout(describe_layout)

        item_label_layout.addWidget(item_label)
        describe_layout.addWidget(self.describe_label)

        item_layout.addLayout(icon_layout)
        item_layout.addLayout(label_layout,1)

        # item_layout.setStretch(0,1)  # 添加伸縮因子

        # 設置項目的布局
        widget = QWidget()
        # 將 itemFrame 設置為 widget 的子 widget
        widget.setLayout(item_layout)

        item.setSizeHint(widget.sizeHint())

        # 將項目添加到 QListWidget
        item.setData(Qt.UserRole, option)  # 使用setData將選項存儲為UserRole
        self.list_widget.addItem(item)
        # self.list_widget.setFont(font)
        self.list_widget.setItemWidget(item, widget)  # 將 widget 與 item 關聯起來


        # 設置點擊事件處理函數，連接點擊信號
        self.list_widget.itemClicked.connect(lambda item: self.handle_record_item_click(item))

        #endregion
    #endregion

    #region 清單描述
    def itemDescribe(self, describe):
        self.describe_label.setText(describe)
    #region 非模組化寫法
    # def itemDescribe(self, option):    
        # #region 「設定」清單
        # if option == '顯示':
        #     self.describe_label.setText('波形圖週期、單位')
        # elif option == '警報輸出':
        #     self.describe_label.setText('Relay 1、Relay 2、Relay 3…')
        # elif option == '類比輸出':
        #     self.describe_label.setText('濃度、溫度、類型')
        # elif option == '感測器溫度保護':
        #     self.describe_label.setText('狀態、溫度設定')
        # elif option == '診斷':
        #     self.describe_label.setText('觀看詳細數值')
        # elif option == '通訊':
        #     self.describe_label.setText('RS-485、HTTP/TCPIP')
        # elif option == '時間':
        #     self.describe_label.setText('調整時間、日期格式')
        # elif option == '語言':
        #     self.describe_label.setText('多國語言')
        # #endregion
            
        # #region 「校正」清單
        # elif option =='感測器校正':
        #     self.describe_label.setText('空氣校正、直接校正')
        # elif option =='大氣壓力校正':
        #     self.describe_label.setText('大氣壓力校正')
        # elif option == '類比輸出校正':
        #     self.describe_label.setText('0 - 20 mA、4 - 20 mA')
        # #endregion
        
        # #region 「記錄」清單
        # elif option == '觀看記錄':
        #     self.describe_label.setText('時間、數值')
        # elif option == '統計表':
        #     self.describe_label.setText('最高值、平均值、最底值')
        # elif option == '下載記錄至隨身碟':
        #     self.describe_label.setText('儲存格式：Excel、txt、json、csv')
        # elif option == '記錄方式設定':
        #     self.describe_label.setText('自動、手動')
        # #endregion
            
        # #region 「識別」清單
        # elif option == '登入身份':
        #     self.describe_label.setText('輸入密碼')
        # elif option == '儀器資訊':
        #     self.describe_label.setText('型號、序號、生產日期……')
        # elif option == '感測器資訊':
        #     self.describe_label.setText('型號、序號、生產日期……')
        # #endregion

        # #region 其他
        # else :
        #     self.describe_label.setText('描述')
        # #endregion
    #endregion
            
    #endregion


    # 在 MyWindow 類別中新增一個槽函數處理 '' 頁面 item 被點擊的信號
    #region 前往下個畫面
    def handle_record_item_click(self, item):
        # 在這裡處理四個功能頁面下 item 被點擊的事件
        # 例如，切換到 testEndFrame 並顯示被點擊的項目文字
        item_text = item.data(Qt.UserRole)

        # 判斷是否已經創建了 testEndFrame
        if item_text not in self.sub_pages: #"testEndFrame"
            print('進入選項：', item_text)

            #region 「設定」
            if item_text == '顯示':
                # 由「設定」進入「顯示」介面
                next_frame = displayOptionFrame(item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages)

            elif item_text == '警報輸出':
                # 由「設定」進入「警報輸出」介面
                next_frame = setAlarmRelayMenuFrame(item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages)
            
            elif item_text == '類比輸出':
                # 由「設定」進入「類比輸出」介面
                next_frame = analogyOutputOptionFrame(item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages)

            elif item_text == '感測器溫度保護':
                # 由「設定」進入「感測器溫度保護」介面
                next_frame = setSensorTempLimitFrame(item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages)

            elif item_text == '通訊':
                # 由「設定」進入「通訊」介面
                next_frame = comOptionFrame(item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages)
                
            elif item_text == '時間':
                # 由「設定」進入「時間」介面
                next_frame = setTimeFrame(item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages)
            #endregion
                
            #region 「校正」
            elif item_text == '類比輸出校正':
                # 由「校正」進入「類比輸出校正」介面
                next_frame = calibrateAnalogyOutputFrame(item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages)
            #endregion
                
            #region 「記錄」
            elif item_text == '下載記錄至隨身碟':
                # 由「設定」進入「時間」介面
                next_frame = recordDownloadFileFrame(item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages)
            #endregion
                
            #region 「識別」
            elif item_text == '登入身份':
                # 由「識別」進入「登入身份」介面，此功能須再與解鎖功能區分
                # next_frame = id_LogIn_Frame(item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages)
                next_frame = testEndFrame(item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages)

            elif item_text == '儀器資訊': 
                # 由「識別」進入「儀器資訊」介面，暫以本機開發硬體測試
                next_frame = deviceInfoFrame(item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages)
            #endregion

            else:
                # 如果還沒有，則創建一個新的 testEndFrame 為終節點畫面測試
                next_frame = testEndFrame(item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages)
                
            # 添加到堆疊中
            next_frame_index = self.stacked_widget.addWidget(next_frame)
            self.sub_pages[item_text] = next_frame_index
        else:
            # 如果已經存在，取得 下一頁（testEndFrame） 的索引
            next_frame_index = self.sub_pages[item_text]

        # 設定當前顯示的子畫面索引為 testEndFrame
        self.stacked_widget.setCurrentIndex(next_frame_index)
        self.current_page_index = next_frame_index

        # print('Current Page Index:', self.current_page_index)
        
        
    #endregion
