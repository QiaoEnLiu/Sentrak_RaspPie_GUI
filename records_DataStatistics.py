#zh-tw
# records_DataStatistics.py

# 此程式碼為觀看記錄、統計表設定時間區間的介面
    
try:
    import traceback
    from PyQt5.QtCore import Qt, QDate
    from PyQt5.QtWidgets import QWidget, QLabel, QDateEdit, QVBoxLayout,QHBoxLayout, QPushButton
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()
class records_DataStatisticsFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages):
        super().__init__()
        print(title)

        self.sub_pages=sub_pages
        
        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(24)
        title_label.setFont(font)
        # title_label.setStyleSheet(_style)

        font.setPointSize(18)
        # user_label = QLabel(PPV.presentUser.userInfo())
        # user_label.setFont(font)
        # user_label.setStyleSheet(_style)

        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        # main_layout.setSpacing(0) 
        main_layout.addWidget(title_label)
        # main_layout.addWidget(user_label)

        setRecordTimeLayout = QVBoxLayout()

        setStartLayout = QVBoxLayout()
        startLabelLayout = QVBoxLayout()
        startTimeLayout = QVBoxLayout()
        startLabel = QLabel("啟始時間：")
        startLabel.setFont(font)
        self.startTime = QDateEdit(calendarPopup=True, date = QDate.currentDate())
        # self.startTime.setMinimumDate(QDate(2000, 1, 1))
        # self.startTime.setMaximumDate(QDate(2025, 12, 31))
        # self.startTime.setStyleSheet('Fusion')
        self.startTime.setFont(font)
        startLabelLayout.addWidget(startLabel)
        startTimeLayout.addWidget(self.startTime)
        setStartLayout.addLayout(startLabelLayout)
        setStartLayout.addLayout(startTimeLayout)

        setEndLayout = QVBoxLayout()
        endLabelLayout = QVBoxLayout()
        endTimeLayout = QVBoxLayout()
        endLabel = QLabel("結束時間：")
        endLabel.setFont(font)
        self.endTime = QDateEdit(calendarPopup=True, date = QDate.currentDate())
        self.endTime.setFont(font)
        setEndLayout.addWidget(endLabel)
        setEndLayout.addWidget(self.endTime)
        setEndLayout.addLayout(endLabelLayout)
        setEndLayout.addLayout(endTimeLayout)

        setLayout = QVBoxLayout()
        set_button = QPushButton('設定區間', self)
        set_button.setFont(font)
        setLayout.addWidget(set_button)

        setRecordTimeLayout.addStretch()
        setRecordTimeLayout.addLayout(setStartLayout)
        setRecordTimeLayout.addStretch()
        setRecordTimeLayout.addLayout(setEndLayout)
        setRecordTimeLayout.addStretch()
        setRecordTimeLayout.addLayout(setLayout)

        main_layout.addLayout(setRecordTimeLayout)


        print(f'{title}畫面')

        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{title} Index: {self.stacked_widget.count()}')


class CustomDateEdit(QDateEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def showPopup(self):
        self.calendarWidget().show()
        self.calendarWidget().raise_()
        self.calendarWidget().activateWindow()
        
        # 顯示年份和月份選擇
        self.calendarWidget().showNavigationBar()
        self.calendarWidget().showMonth()