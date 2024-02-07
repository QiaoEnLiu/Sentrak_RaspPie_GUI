#zh-tw
# setAnalogyOutputOption.py
# 「類比輸出」

# 此程式碼為「設定」底下的「類比輸出」選項
    # 「類比濃度」為進入濃度類比訊號的設定
    # 「類比溫度」為進入溫度類比訊號的設定

try:
    import traceback
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy
    from PyQt5.QtGui import QFont

    from setAnalogyTemp import analogyTempFrame
    from setAnalogyConcentration import analogyConcentrationFrame
    
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")


font = QFont()

class analogyOutputOptionFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages):
        super().__init__()
        self.title=title
        self.stacked_widget=stacked_widget
        self.sub_pages=sub_pages

        # print(self.title,ProjectPublicVariable.presentUser.userInfo())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0) 

        title_layout =QVBoxLayout()
        # title_layout.setContentsMargins(0, 0, 0, 0) 
        # title_layout.setSpacing(0)
        analogyTemp_layout = QVBoxLayout()
        analogyConcentration_layout = QVBoxLayout()
        analogyOption_layout =QVBoxLayout()
                
        self.title_label = QLabel(self.title, self)
        self.title_label.setAlignment(Qt.AlignCenter)  
        self.title_label.setContentsMargins(0, 0, 0, 0)
        font.setPointSize(72)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet(_style)


        font.setPointSize(54)
        analogyConcentrationBTN=QPushButton('類比濃度', self)
        analogyConcentrationBTN.setFont(font)
        # analogyConcentrationBTN.setStyleSheet(_style)
        analogyConcentrationBTN.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        analogyTempBTN=QPushButton('類比溫度', self)
        analogyTempBTN.setFont(font)
        # analogyTempBTN.setStyleSheet(_style)
        analogyTempBTN.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        title_layout.addWidget(self.title_label)
        analogyConcentration_layout.addWidget(analogyConcentrationBTN)
        analogyTemp_layout.addWidget(analogyTempBTN)
        # analogyOption_layout.addStretch()
        analogyOption_layout.addLayout(analogyConcentration_layout)
        # analogyOption_layout.addStretch()
        analogyOption_layout.addLayout(analogyTemp_layout)


        main_layout.addLayout(title_layout)
        # main_layout.addStretch()
        main_layout.addLayout(analogyOption_layout)

        # print(user.userInfo())

        displayOption_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = displayOption_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{self.title} Index: {self.stacked_widget.count()}')
        
        analogyConcentrationBTN.clicked.connect(lambda:self.analogyOptionClick(analogyConcentrationBTN.text(),self.title_label.styleSheet()))
        analogyTempBTN.clicked.connect(lambda:self.analogyOptionClick(analogyTempBTN.text(),self.title_label.styleSheet()))

    
    def analogyOptionClick(self, option, _style):
        if option not in self.sub_pages or not self.stacked_widget.widget(self.sub_pages[option]):
            print(f'進入：{option}')
            if option == '類比濃度': # 類比濃度
                next_frame = analogyTempFrame(option, _style, self.stacked_widget, self.sub_pages)
            elif option == '類比溫度': # 類比溫度
                next_frame = analogyConcentrationFrame(option, _style, self.stacked_widget, self.sub_pages)
            else:
                print('Wrong Option:',option)

            next_frame_index = self.stacked_widget.addWidget(next_frame)
            self.sub_pages[option] = next_frame_index
        else:
            next_frame_index = self.sub_pages[option]

        self.stacked_widget.setCurrentIndex(next_frame_index)
        self.current_page_index = next_frame_index
