#zh-tw
# setAlarmRelay.py

# 此程式碼為進入Relay設定的選單（暫時分三個程式，未來會以模組化修改）
    # Relay1 >> setAlarmRelay1.py
    # Relay2 >> setAlarmRelay2.py
    # Relay3 >> setAlarmRelay3.py

try:
    import traceback
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
    from imgResource import setLabelIcon

    from setAlarmRelay import setAlarmRelayFrame
    from setAlarmRelay2 import setAlarmRelay2Frame
    from setAlarmRelay3 import setAlarmRelay3Frame


    # 未實作功能測試介面
    from testEndFrame import testEndFrame
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()
itemTitleSize = QFont()
itemTitleSize.setPointSize(20)
itemdescribeSize = QFont()
itemdescribeSize.setPointSize(14)
class setAlarmRelayMenuFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages):
        super().__init__()
        print(title)


        self.sub_pages=sub_pages
        
        self.title_label = QLabel(title, self)
        self.title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(32)
        self.title_label.setFont(font)
        # self.title_label.setStyleSheet(_style)

        font.setPointSize(24)
        # user_label = QLabel(PPV.presentUser.userInfo())
        # user_label.setFont(font)
        # user_label.setStyleSheet(_style)

        self.relayList_widget = QListWidget(self)
        for option in PPV.relays:
            self.create_list_item(option)
            self.itemDeescribe(option)

        content_layout = QVBoxLayout()
        content_layout.addWidget(self.relayList_widget)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0) 
        main_layout.addWidget(self.title_label)
        # main_layout.addWidget(user_label)
        main_layout.addLayout(content_layout)

        
        print('警報輸出測試畫面：', title)

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
    def itemDeescribe(self, option):
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
            next_frame = setAlarmRelayFrame(item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages)

            # #region 「relay」
            # if item_text == 'relay1':
            #     # 由「設定relay選單」進入「relay1」介面
            #     next_frame = setAlarmRelayFrame(item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages)

            # elif item_text == 'relay2':
            #     # 由「設定relay選單」進入「relay2」介面
            #     next_frame = setAlarmRelay2Frame(item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages)
            
            # elif item_text == 'relay3':
            #     # 由「設定relay選單」進入「relay3」介面
            #     next_frame = setAlarmRelay3Frame(item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages)
            # else:
            #     # 如果還沒有，則創建一個新的 testEndFrame 為終節點畫面測試
            #     next_frame = testEndFrame(item_text, self.title_label.styleSheet(), self.stacked_widget, self.sub_pages)
            # # 添加到堆疊中
            # #endregion    
            next_frame_index = self.stacked_widget.addWidget(next_frame)
            self.sub_pages[item_text] = next_frame_index
        else:
            # 如果已經存在，取得 下一頁（testEndFrame） 的索引
            next_frame_index = self.sub_pages[item_text]

        # 設定當前顯示的子畫面索引為 testEndFrame
        self.stacked_widget.setCurrentIndex(next_frame_index)
        self.current_page_index = next_frame_index

    #endregion
