#zh-tw
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QCalendarWidget, QVBoxLayout, QWidget, QLineEdit
from PyQt5.QtCore import Qt


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Main Window')

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(100, 50, 100, 30)
        self.lineEdit.setPlaceholderText("Click me to open calendar")
        self.lineEdit.mousePressEvent = self.openCalendar  # 將 mousePressEvent 設置為 openCalendar 函數

    def openCalendar(self, event):
        # if event.button() == Qt.LeftButton:
            calendar = QCalendarWidget()
            calendar.setGridVisible(True)

            layout = QVBoxLayout()
            layout.addWidget(calendar)

            widget = QWidget()
            widget.setLayout(layout)

            msgBox = QMessageBox()
            msgBox.setWindowTitle('Select Date')
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText('Select a date:')
            msgBox.addButton(QMessageBox.Ok)
            msgBox.setStandardButtons(QMessageBox.Cancel)
            msgBox.layout().addWidget(widget)
            msgBox.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainApp()
    mainWindow.show()
    sys.exit(app.exec_())
