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

        self.recordStart = ""
        self.recordEnd = ""

        self.dateFormat = PPV.dateFormat[int(PySQL.selectSQL_Reg(4, 1))][1]

        if self.title == '觀看記錄':
            self.recordStart = 'recordDataStart'
            self.recordEnd = 'recordDataEnd'
        elif self.title == '統計表':
            self.recordStart = 'recordStatisticsStart'
            self.recordEnd = 'recordStatisticsEnd'


        self.cacheStartDate = PySQL.selectSQL_Var(self.recordStart)
        self.cacheEndDate = PySQL.selectSQL_Var(self.recordEnd)


        if self.cacheStartDate is None:
            self.cacheStartDate = PPV.current_datetime.toString(self.dateFormat)
        
        if self.cacheEndDate is None:
            self.cacheEndDate = PPV.current_datetime.toString(self.dateFormat)
        
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
        self.startDate = QLineEdit(self.cacheStartDate)
        # self.startDate.setPlaceholderText(self.cacheStartDate)
        self.startDate.mousePressEvent = self.openDialogCalendar(self.startDate)
        
        
        self.startDate.setFont(font)
        setStartLayout.addWidget(self.startLabel)
        setStartLayout.addWidget(self.startDate)


        setEndLayout = QVBoxLayout()
        self.endLabel = QLabel("結束時間：")
        self.endLabel.setFont(font)
        self.endDate = QLineEdit(self.cacheEndDate)
        # self.endDate.setPlaceholderText(self.cacheEndDate)
        self.endDate.mousePressEvent = self.openDialogCalendar(self.endDate)
        
        
        
        self.endDate.setFont(font)
        setEndLayout.addWidget(self.endLabel)
        setEndLayout.addWidget(self.endDate)

        # self.startDate.dateChanged.connect(self.updateEndDate)
        # self.endDate.dateChanged.connect(self.checkEndDate)

        setLayout = QVBoxLayout()
        set_button = QPushButton('確認區間', self)
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

    def openDialogCalendar(self, line_edit):
        def handle_event(event):
            if event.button() == Qt.LeftButton:
                selected_date = self.selectDateFromDialog()
                if selected_date:
                    line_edit.setText(selected_date)

        return handle_event

    def selectDateFromDialog(self):
        dialog = CalendarDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            return dialog.calendar.selectedDate().toString(self.dateFormat)
        return None

    
    def setDateInterval(self):
        selectStartDate = self.startDate.text()
        selectEndDate = self.endDate.text()

        print(f"Start:{self.recordStart}")
        print(f"End:{self.recordEnd}")

        if selectStartDate and selectEndDate:
            if QDate.fromString(selectStartDate, self.dateFormat) > QDate.fromString(selectEndDate, self.dateFormat):
                # 開始日期在結束日期之後，交換它們
                selectStartDate, selectEndDate = selectEndDate, selectStartDate
                self.startDate.setText(selectStartDate)
                self.endDate.setText(selectEndDate)

        setIntervalInfo = "\n\r" + \
                        self.title + "：\n\r" + \
                        self.startLabel.text() + selectStartDate + "\n\r" + \
                        self.endLabel.text() + selectEndDate  + "\n\r"
        print(setIntervalInfo)
        PySQL.updateSQL_Var(self.recordStart, selectStartDate)
        PySQL.updateSQL_Var(self.recordEnd, selectEndDate)

#region CalendarDialog
class CalendarDialog(QDialog):
    
    def __init__(self, parent=None):
        super(CalendarDialog, self).__init__(parent)
        self.setWindowTitle('Select Date')
        font.setPointSize(20)

        self.selectedDateLabel = QLabel("選擇時間：")
        self.selectedDateLabel.setAlignment(Qt.AlignLeft)
        self.selectedDateLabel.setFont(font)

        font.setPointSize(16)
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        # self.calendar.setNavigationBarVisible(True)
        self.calendar.setFont(font)

        #region 以下客製化樣式是解決年份及月份未顯示的問題
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: black;
                border: 2px solid #000000;
            }

            QCalendarWidget QToolButton {
                color: #000000;
                font-weight: bold;
            }

            QCalendarWidget QToolButton:hover {
                background-color: #2a82da;
                color: black;
            }
            
            QCalendarWidget QMenu {
                background-color: white;
            }

            QCalendarWidget QMenu::item {
                color: black;
            }

            QCalendarWidget QMenu::item:selected {
                background-color: #2a82da;
            }
                                    
            QCalendarWidget QAbstractItemView:enabled {
                color: black;
            }

            QCalendarWidget QAbstractItemView:enabled:hover {
                background-color: #2a82da;
                color: black;
            }

            QCalendarWidget QAbstractItemView:enabled:selected {
                background-color: #2a82da;
                color: black;
            }


            QCalendarWidget QSpinBox {
                width: 60px;
            }
                                    
                                     

        """)
        #endregion

        layout = QVBoxLayout(self)
        layout.addWidget(self.selectedDateLabel)
        layout.addWidget(self.calendar)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout.addWidget(buttonBox)

        widget = QWidget()
        widget.setLayout(layout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(widget)

        self.setFixedSize(480, 360)

        self.setLayout(mainLayout)

    def accept(self):
        selectedDate = self.calendar.selectedDate()
        # print("Selected Date:", selectedDate.toString("yyyy-MM-dd"))
        super(CalendarDialog, self).accept()
        return selectedDate
#endregion




