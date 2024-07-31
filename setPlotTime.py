#zh-tw
# setPlotTime.py
# 「波形圖週期」

# 此程式碼為「顯示」底下的「波形圖週期」介面
    # 設定折線圖顯示的時間單位（尚未套用於折線圖上）

try:
    import traceback
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton, QMessageBox
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
    import PySQL
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()
class setPlotTimeFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages):
        super().__init__()
        print(title)

        self.sub_pages = sub_pages
        
        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(36)
        title_label.setFont(font)
        # title_label.setStyleSheet(_style)

        # user_label = QLabel(user.userInfo())
        # user_label.setFont(font)
        # user_label.setStyleSheet(_style)

        self.plot_time_combo = QComboBox()
        self.plot_time_combo.setFont(font)
        self.plot_time_combo.addItems(PPV.plotTimeDict.values()) # ['1分','5分','10分','30分','1小時']
        # default_plotTime_Index = self.plot_time_combo.findText(PPV.plotTimeDict[int(PySQL.selectSQL_Var('plotTime'))])
        self.plot_time_combo.setCurrentIndex(self.plot_time_combo.findText(PPV.plotTime))

        set_button = QPushButton('確認', self)
        set_button.setFont(font)
        set_button.clicked.connect(self.setPlotTimes)
        
        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        # main_layout.setSpacing(0) 

        set_time_layout = QVBoxLayout()
        # set_time_layout.setContentsMargins(0, 0, 0, 0)
        # set_time_layout.setSpacing(0)
        set_time_layout.addWidget(self.plot_time_combo)
        set_time_layout.addStretch()
        set_time_layout.addWidget(set_button)

        main_layout.addWidget(title_label)
        # main_layout.addStretch()
        main_layout.addLayout(set_time_layout)
        # main_layout.addWidget(user_label)

        # print('終節點測試畫面：', title)

        self.stacked_widget = stacked_widget
        setPlotTime_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = setPlotTime_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{title} Index: {self.stacked_widget.count()}')

    def setPlotTimes(self):


        if QMessageBox.question(self, '顯示波形圖週期', f'設定波形圖週期：由 每{PPV.plotTime} 改成 每{self.plot_time_combo.currentText()}\
                                \n確定要設定波形圖週期嗎？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
            action = '確認'
            # 在這裡添加您想要在使用者點擊"Yes"時執行的程式碼
            PPV.plotTime = self.plot_time_combo.currentText()
            # self.plot_time_combo.setCurrentIndex(PPV.plotTime)
            print(f'更改波形圖週期為：{PPV.plotTime}({PPV.get_keys_from_value(PPV.plotTimeDict, PPV.plotTime)[0]})')
            PySQL.updateSQL_Var('plotTime', PPV.get_keys_from_value(PPV.plotTimeDict, PPV.plotTime)[0])


            print("使用者設定波形圖週期")

        else:
            action = '取消'
        