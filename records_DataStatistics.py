#zh-tw
# records_DataStatistics.py

# 此程式碼為觀看記錄、統計表設定時間區間的介面
    
try:
    import traceback
    from PyQt5.QtCore import Qt, QDate
    from PyQt5.QtWidgets import QWidget, QLabel,QLineEdit, QDateEdit, QVBoxLayout, QHBoxLayout, QPushButton, QCalendarWidget, QDialogButtonBox, QDialog, QMessageBox, QDateTimeEdit
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
    import PySQL
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()
class records_DataStatisticsFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages):
        super().__init__()
        print(title)

        self.sub_pages = sub_pages
        self.title = title

        self.dateFormat = PPV.dateFormat[int(PySQL.selectSQL_Reg(4, 1))][1]
        
        title_label = QLabel(self.title)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(24)
        title_label.setFont(font)
        # title_label.setStyleSheet(_style)

        font.setPointSize(20)
        # user_label = QLabel(PPV.presentUser.userInfo())
        # user_label.setFont(font)
        # user_label.setStyleSheet(_style)

        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        # main_layout.setSpacing(0) 
        main_layout.addWidget(title_label)
        # main_layout.addWidget(user_label)

        setRecordDateLayout = QVBoxLayout()

        setStartLayout = QVBoxLayout()
        self.startLabel = QLabel("啟始時間：")
        self.startLabel.setFont(font)
        self.startDate = QLineEdit()
        self.startDate.setPlaceholderText("Click me to open calendar")
        self.startDate.mousePressEvent = self.openDialogCalendar
        
        
        self.startDate.setFont(font)
        setStartLayout.addWidget(self.startLabel)
        setStartLayout.addWidget(self.startDate)


        setEndLayout = QVBoxLayout()
        self.endLabel = QLabel("結束時間：")
        self.endLabel.setFont(font)
        self.endDate = QLineEdit()
        self.endDate.setPlaceholderText("Click me to open calendar")
        self.endDate.mousePressEvent = self.openDialogCalendar
        
        self.endDate.setFont(font)
        setEndLayout.addWidget(self.endLabel)
        setEndLayout.addWidget(self.endDate)

        # self.startDate.dateChanged.connect(self.updateEndDate)
        # self.endDate.dateChanged.connect(self.checkEndDate)

        setLayout = QVBoxLayout()
        set_button = QPushButton('設定區間', self)
        set_button.clicked.connect(self.setDateInterval)
        set_button.setFont(font)
        setLayout.addWidget(set_button)

        setRecordDateLayout.addStretch()
        setRecordDateLayout.addLayout(setStartLayout)
        setRecordDateLayout.addStretch()
        setRecordDateLayout.addLayout(setEndLayout)
        setRecordDateLayout.addStretch()
        setRecordDateLayout.addLayout(setLayout)

        main_layout.addLayout(setRecordDateLayout)


        print(f'{title}畫面')

        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{title} Index: {self.stacked_widget.count()}')

    def openDialogCalendar(self, event):
        if event.button() == Qt.LeftButton:  # 檢查是否是左鍵按下
            dialog = CalendarDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                print("User clicked OK")
            else:
                print("User clicked Cancel")

    def openMessageCalendar(self, event):
        if event.button() == Qt.LeftButton:  # 檢查是否是左鍵按下
            dialog = CalendarMessageBox(self)
            if dialog.exec_() == QDialog.Accepted:
                print("User clicked OK")
            else:
                print("User clicked Cancel")
    
    def updateEndDate(self, date):
        self.endDate.setMinimumDate(date)
    
    def checkEndDate(self, date):
        min_date = self.startDate.date()
        if date < min_date:
            self.endDate.setDate(min_date)
    
    def setDateInterval(self):
        selectStartDate = self.startDate.date().toString(self.dateFormat)
        selectEndDate = self.endDate.date().toString(self.dateFormat)

        setIntervalInfo = "\n\r" + \
                        self.title + "：\n\r" + \
                        self.startLabel.text() + selectStartDate + "\n\r" + \
                        self.endLabel.text() + selectEndDate  + "\n\r"
        print(setIntervalInfo)

class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super(CalendarDialog, self).__init__(parent)
        self.setWindowTitle('Select Date')

        # self.selectedDateLabel = QLabel("選擇時間：")
        # self.selectedDateLabel.setAlignment(Qt.AlignLeft)

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setNavigationBarVisible(True)

        self. calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: white;
                border: 2px solid #2a82da;
            }

            QCalendarWidget QToolButton {
                color: #2a82da;
                font-weight: bold;
            }

            QCalendarWidget QToolButton:hover {
                background-color: #2a82da;
                color: white;
            }

            QCalendarWidget QToolButton#qt_calendar_prevmonth {
                qproperty-icon: url(:/qss_icons/rc/arrow_left.png);
            }

            QCalendarWidget QToolButton#qt_calendar_nextmonth {
                qproperty-icon: url(:/qss_icons/rc/arrow_right.png);
            }

            QCalendarWidget QSpinBox {
                width: 60px;
            }
        """)

        layout = QVBoxLayout(self)
        # layout.addWidget(self.selectedDateLabel)
        layout.addWidget(self.calendar)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout.addWidget(buttonBox)

        widget = QWidget()
        widget.setLayout(layout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(widget)

        self.setFixedSize(480, 280)

        self.setLayout(mainLayout)

    def accept(self):
        selectedDate = self.calendar.selectedDate()
        print("Selected Date:", selectedDate.toString("yyyy-MM-dd"))
        super(CalendarDialog, self).accept()

class CalendarMessageBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('選擇日期')

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.setText('選擇日期:')
        self.layout().addWidget(self.calendar)

    def selectedDate(self):
        return self.calendar.selectedDate()



