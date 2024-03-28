from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QIntValidator

class lineEditOnlyInt(QLineEdit):
    def __init__(self, parent=None):
        super(lineEditOnlyInt, self).__init__(parent)
        
        # 使用 QIntValidator 限制輸入只能是整數
        validator = QIntValidator()
        self.setValidator(validator)
        