import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QDateEdit, QLabel
from PyQt5.QtGui import QFont


font = QFont()
class DateSelector(QWidget):
    def __init__(self):
        super().__init__()

        font.setPointSize(24)
        main_layout = QVBoxLayout(self)
        layout = QVBoxLayout()

        self.dateTitle = QLabel("日期")
        self.dateTitle.setFont(font)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)  # 啟用彈出式日曆
        self.date_edit.setDate(self.date_edit.calendarWidget().selectedDate())  # 設置默認日期
        self.date_edit.dateChanged.connect(self.on_date_changed)  # 連接日期更改的信號
        self.date_edit.setFont(font)

        layout.addWidget(self.dateTitle)
        layout.addWidget(self.date_edit)
        main_layout.addLayout(layout)
        #self.setLayout(layout)

    def on_date_changed(self, date):
        print("選擇的日期:", date.toString("yyyy-MM-dd"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DateSelector()
    window.show()
    sys.exit(app.exec_())
