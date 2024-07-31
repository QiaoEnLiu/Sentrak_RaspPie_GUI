#zh-tw
# setAlarmRelay2.py

# 此程式碼為設定Relay2

try:
    import traceback
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit, QPushButton
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()
class setAlarmRelay2Frame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages, mainTitle):
        super().__init__()
        print(title)

        self.sub_pages=sub_pages
        
        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        # title_label.setContentsMargins(0, 0, 0, 0)
        font.setPointSize(32)
        title_label.setFont(font)
        # title_label.setStyleSheet(_style)


        font.setPointSize(20)
        # user_label = QLabel(PPV.presentUser.userInfo())
        # user_label.setFont(font)
        # user_label.setStyleSheet(_style)

        relayStateLabel = QLabel(f"{title}狀態：")
        relayStateLabel.setFont(font)
        relayStateCombox = QComboBox()
        relayStateCombox.setFont(font)
        relayStateCombox.addItems(['啟用', '停用'])

        meassureTypeLabel = QLabel("測量類型：")
        meassureTypeLabel.setFont(font)
        meassureTypeCombox = QComboBox()
        meassureTypeCombox.setFont(font)
        meassureTypeCombox.addItems(['濃度', '溫度'])

        switchTypeLabel = QLabel("接觸點型式：")
        switchTypeLabel.setFont(font)
        switchTypeCombox = QComboBox()
        switchTypeCombox.setFont(font)
        switchTypeCombox.addItems(['常開', '常關'])

        valueLimitTypeLabel = QLabel("數值判別：")
        valueLimitTypeLabel.setFont(font)
        valueLimitTypeCombox = QComboBox()
        valueLimitTypeCombox.setFont(font)
        valueLimitTypeCombox.addItems(['高於', '低於'])

        valueLabel = QLabel("數值：")
        valueLabel.setFont(font)
        valueInput = QLineEdit()
        valueInput.setFont(font)

        set_button = QPushButton('確認', self)
        set_button.setFont(font)


        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        # main_layout.setSpacing(0) 
        main_layout.addWidget(title_label)
        # main_layout.addWidget(user_label)




        relayStateLayout = QHBoxLayout()
        relayStateLeft = QVBoxLayout()
        relayStateRight = QVBoxLayout()
        relayStateLeft.addWidget(relayStateLabel)
        relayStateRight.addWidget(relayStateCombox)
        relayStateLayout.addLayout(relayStateLeft)
        relayStateLayout.addLayout(relayStateRight)

        meassureTypeLayout = QHBoxLayout()
        meassureTypeLeft = QVBoxLayout()
        meassureTypeRight = QVBoxLayout()
        meassureTypeLeft.addWidget(meassureTypeLabel)
        meassureTypeRight.addWidget(meassureTypeCombox)
        meassureTypeLayout.addLayout(meassureTypeLeft)
        meassureTypeLayout.addLayout(meassureTypeRight)

        switchTypeLayout = QHBoxLayout()
        switchTypeLeft = QVBoxLayout()
        switchTypeRight = QVBoxLayout()
        switchTypeLeft.addWidget(switchTypeLabel)
        switchTypeRight.addWidget(switchTypeCombox)
        switchTypeLayout.addLayout(switchTypeLeft)
        switchTypeLayout.addLayout(switchTypeRight)
        
        valueLimitTypeLayout = QHBoxLayout()
        valueLimitTypeLeft = QVBoxLayout()
        valueLimitTypeRight = QVBoxLayout()
        valueLimitTypeLeft.addWidget(valueLimitTypeLabel)
        valueLimitTypeRight.addWidget(valueLimitTypeCombox)
        valueLimitTypeLayout.addLayout(valueLimitTypeLeft)
        valueLimitTypeLayout.addLayout(valueLimitTypeRight)

        valueLayout = QHBoxLayout()
        valueLeft = QVBoxLayout()
        valueRight = QVBoxLayout()
        valueLeft.addWidget(valueLabel)
        valueRight.addWidget(valueInput)
        valueLayout.addLayout(valueLeft)
        valueLayout.addLayout(valueRight)


        setLayout = QVBoxLayout()
        setLayout.addWidget(set_button)


        main_layout.addLayout(relayStateLayout)
        main_layout.addLayout(meassureTypeLayout)
        main_layout.addLayout(switchTypeLayout)
        main_layout.addLayout(valueLimitTypeLayout)
        main_layout.addLayout(valueLayout)
        main_layout.addLayout(setLayout)


        print('警報Relay1測試畫面：', title)

        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{title} Index: {self.stacked_widget.count()}')