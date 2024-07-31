#zh-tw
# setAlarmRelay.py

try:
    import traceback
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
    from imgResource import setLabelIcon

    import subMenuDict

    '''# 設定 >>
    from setUnit import setUnitFrame # 「介面」>>「單位」
    from setPlotTime import setPlotTimeFrame # 「介面」>>「波形圖週期」

    from setAlarmRelay import setAlarmRelayFrame # 「警報輸出」>>「Relay 1」、「Relay 2」、「Relay 3」
    # from setAlarmRelay2 import setAlarmRelay2Frame
    # from setAlarmRelay3 import setAlarmRelay3Frame

    from setAnalogyOutput import setAnalogyOutputFrame # 「類比輸出」>>「類比濃度」、「類比溫度」
    # from setAnalogyTemp import analogyTempFrame
    # from setAnalogyConcentration import analogyConcentrationFrame

    from set_HTTP_TCPIP import internetFrame # 「通訊」>>「HTTP / TCPIP」
    from set_RS485 import rs485_Frame # 「通訊」>>「RS485」

    # 校正 >>
    from calibrateAirManual import calibrateAirManualFrame # 「感測器校正」>>「直接校正」、「空氣校正」

    # 記錄 >>

    # 識別 >>

    # 未實作功能測試介面
    from testEndFrame import testEndFrame'''

except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()
itemTitleSize = QFont()
itemTitleSize.setPointSize(20)
itemdescribeSize = QFont()
itemdescribeSize.setPointSize(10)
class subOptionFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages, mainTitle):
        super().__init__()
        print(title)

        self.mainTitle=mainTitle
        self.title=title

        self.sub_pages=sub_pages
        
        self.title_label = QLabel(self.title, self)
        self.title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(32)
        self.title_label.setFont(font)
        # self.title_label.setStyleSheet(_style)

        font.setPointSize(24)
        # user_label = QLabel(PPV.presentUser.userInfo())
        # user_label.setFont(font)
        # user_label.setStyleSheet(_style)

        self.relayList_widget = QListWidget(self)
        for option, value in subMenuDict.subMenu[self.mainTitle][self.title][2].items():
            self.create_list_item(option)
            self.itemDescribe(value[0])

        '''if title == '顯示':
            for option in PPV.subDisplay:
                self.create_list_item(option)
                self.itemDeescribe(option)

        elif title == '警報輸出':
            for option in PPV.relays:
                self.create_list_item(option)
                self.itemDeescribe(option)
            
        elif title == '類比輸出':
            for option in PPV.subAnalogy:
                self.create_list_item(option)
                self.itemDeescribe(option)

        elif title == '通訊':
            for option in PPV.subCommunication:
                self.create_list_item(option)
                self.itemDeescribe(option)

        elif title == '感測器校正':
            for option in PPV.subCalibrateAirManual:
                self.create_list_item(option)
                self.itemDeescribe(option)'''


        content_layout = QVBoxLayout()
        content_layout.addWidget(self.relayList_widget)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0) 
        main_layout.addWidget(self.title_label)
        # main_layout.addWidget(user_label)
        main_layout.addLayout(content_layout)

        
        print('子功能選單測試畫面：', title)

        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{title} Index: {self.stacked_widget.count()}')



    #region 清單內容
    def create_list_item(self, option):

        # 創建 QListWidgetItem
        item = QListWidgetItem()
        
        # 設置清單圖示及其內部配制
        #region 清單圖示

        list_icon = QLabel('圖示')
        list_icon.setStyleSheet("border: 2.5px solid black;border-right: 0px;")

        setLabelIcon(list_icon,'test_icon.png')
        
        item_label = QLabel(option)# 設置文字

        item_label.setFont(itemTitleSize)
        item_label.setStyleSheet("border: 2.5px solid black;")
        item_label.setContentsMargins(0, 0, 0, 0)
        # print('item_label:', item_label.font().pointSize())

        #endregion

        # 設置清單描述配制
        #region 清單描述及其配制
        self.describe_label = QLabel()
        self.describe_label.setText('描述')
        self.describe_label.setFont(itemdescribeSize)
        self.describe_label.setStyleSheet("border: 2.5px solid black;border-top: 0px; color: gray")
        self.describe_label.setContentsMargins(0, 0, 0, 0)
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
        self.relayList_widget.addItem(item)
        # self.list_widget.setFont(font)
        self.relayList_widget.setItemWidget(item, widget)  # 將 widget 與 item 關聯起來


        # 設置點擊事件處理函數，連接點擊信號
        self.relayList_widget.itemClicked.connect(lambda item: self.handle_record_item_click(item))

        #endregion
    #endregion
        
    #region 清單描述
    def itemDescribe(self, option):
        item_title = option
        self.describe_label.setText(item_title)


    #endregion
    #region 前往下個畫面
    def handle_record_item_click(self, item):
        # 在這裡處理四個功能頁面下 item 被點擊的事件
        # 例如，切換到 testEndFrame 並顯示被點擊的項目文字
        item_text = item.data(Qt.UserRole)

        # 判斷是否已經創建了 testEndFrame
        if item_text not in self.sub_pages: #"testEndFrame"
            print('進入選項：', item_text)
            selectOption = subMenuDict.subMenu.get(self.mainTitle,{}).get(self.title,{})[2]
            next_frame = selectOption.get(item_text,{})[1](item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages, self.mainTitle)
            # 添加到堆疊中
            next_frame_index = self.stacked_widget.addWidget(next_frame)
            self.sub_pages[item_text] = next_frame_index
        else:
            # 如果已經存在，取得 下一頁（testEndFrame） 的索引
            next_frame_index = self.sub_pages[item_text]

        # 設定當前顯示的子畫面索引為 testEndFrame
        self.stacked_widget.setCurrentIndex(next_frame_index)
        self.current_page_index = next_frame_index

    #endregion
