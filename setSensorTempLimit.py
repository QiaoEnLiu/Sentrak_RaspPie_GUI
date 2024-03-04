#zh-tw
# testEndFrame.py

# 此程式碼為子畫面最終刷新測試碼
    # 尚未實作的功能介面都會先以此介面顯示
try:
    import traceback
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout,\
                                 QCheckBox, QLineEdit, QPushButton, QMessageBox
    
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")
temp_default='16.80'
unit_default='°C'

font = QFont()
class tsetSensorTempLimitFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages):
        super().__init__()
        print(title)

        self.sub_pages=sub_pages
        
        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(32)
        title_label.setFont(font)
        # title_label.setStyleSheet(_style)

        font.setPointSize(24)
        # user_label = QLabel(PPV.presentUser.userInfo())
        # user_label.setFont(font)
        # user_label.setStyleSheet(_style)


        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        # main_layout.setSpacing(0) 

        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)

        checkbox_layout = QVBoxLayout()
        self.checkbox = QCheckBox('啟用感測器溫度保護', self)
        self.checkbox.setFont(font)
        self.checkbox.setStyleSheet("QCheckBox::indicator"
                               "{"
                               "width : 24px;"
                               "height : 24px;"
                               "}")
        checkbox_layout.addWidget(self.checkbox)

        setTemp_layout = QHBoxLayout()
        self.setTemp_label = QLabel('溫度設定：')
        self.setTemp_label.setFont(font)
        self.inputTemp = QLineEdit(temp_default)
        self.inputTemp.setFont(font)
        self.inputTemp.setEnabled(self.checkbox.isChecked())
        self.tempUnit = QLabel(unit_default)
        self.tempUnit.setFont(font)
        setTemp_layout.addWidget(self.setTemp_label)
        setTemp_layout.addWidget(self.inputTemp)
        setTemp_layout.addWidget(self.tempUnit)

        set_layout = QVBoxLayout()
        set = QPushButton('設定', self)
        set.setFont(font)
        set_layout.addWidget(set)

        main_layout.addLayout(title_layout)
        main_layout.addLayout(checkbox_layout)
        main_layout.addLayout(setTemp_layout)
        main_layout.addLayout(set_layout)

        self.checkbox.stateChanged.connect(lambda: self.inputTemp.setEnabled(self.checkbox.isChecked()))
        set.clicked.connect(self.setTempLimit)


        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{title} Index: {self.stacked_widget.count()}')

    

    def setTempLimit(self):
        # print(self.checkbox.text(), ":", self.checkbox.isChecked())
        # print(self.setTemp_label.text(), self.inputTemp.text(), self.tempUnit.text())

        if self.checkbox.isChecked():
            action = '啟用' if QMessageBox.question(self, '感測器溫度保護', f'設定最高溫度限制：{self.inputTemp.text() + self.tempUnit.text()}\n確定要啟用感測器溫度保護嗎？',
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes else '取消'
        else:
            action = '停用' if QMessageBox.question(self, '感測器溫度保護', f'目前最高溫度限制：{self.inputTemp.text()+ self.tempUnit.text()}\n確定要停用感測器溫度保護嗎？',
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes else '取消'

        QMessageBox.information(self, '感測器溫度保護', f'{action}設定')
