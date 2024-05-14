#zh-tw 我目前很滿意下方的程式碼
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QCalendarWidget, QVBoxLayout, QWidget, QLineEdit, QDialogButtonBox, QLabel
from PyQt5.QtCore import Qt


class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super(CalendarDialog, self).__init__(parent)
        self.setWindowTitle('Select Date')

        self.selectedDateLabel = QLabel("選擇時間：")
        self.selectedDateLabel.setAlignment(Qt.AlignLeft)

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)

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
                                    
                                    
            # QCalendarWidget QToolButton#qt_calendar_prevmonth {
            #     qproperty-icon: url(:/qss_icons/rc/arrow_left.png);
            # }

            # QCalendarWidget QToolButton#qt_calendar_nextmonth {
            #     qproperty-icon: url(:/qss_icons/rc/arrow_right.png);
            # }
        """)

        layout = QVBoxLayout()
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

        self.setLayout(mainLayout)

    def accept(self):
        selectedDate = self.calendar.selectedDate()
        print("Selected Date:", selectedDate.toString("yyyy-MM-dd"))
        super(CalendarDialog, self).accept()


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.initUI()
        mainLayout = QVBoxLayout()
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Main Window')

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(100, 50, 100, 30)
        self.lineEdit.setPlaceholderText("Click me to open calendar")
        self.lineEdit.mousePressEvent = self.openCalendar  # 將 mousePressEvent 設置為 openCalendar 函數
        mainLayout.addWidget(self.lineEdit)


    def initUI(self):
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Main Window')

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(100, 50, 100, 30)
        self.lineEdit.setPlaceholderText("Click me to open calendar")
        self.lineEdit.mousePressEvent = self.openCalendar  # 將 mousePressEvent 設置為 openCalendar 函數

    def openCalendar(self, event):
        if event.button() == Qt.LeftButton:  # 檢查是否是左鍵按下
            dialog = CalendarDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                print("User clicked OK")
            else:
                print("User clicked Cancel")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainApp()
    mainWindow.show()
    sys.exit(app.exec_())
