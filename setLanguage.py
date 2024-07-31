#zh-tw
# setLanguage.py

# 此程式碼設定語言介面

try:
    import traceback
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
    import PySQL
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()
class setLanguageFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages, mainTitle):
        super().__init__()
        print(f"{title}({PPV.languages[int(PySQL.selectSQL_Var('language'))]})")
        PPV.languageName = PPV.languages[int(PySQL.selectSQL_Var('language'))]
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

        self.language_combo = QComboBox()
        self.language_combo.setFont(font)
        self.language_combo.addItems(PPV.languages.values())
        self.language_combo.setCurrentIndex(self.language_combo.findText(PPV.languageName))

        set_button = QPushButton('確認', self)
        set_button.setFont(font)
        set_button.clicked.connect(self.setLanguage)

        set_language_layout = QVBoxLayout()
        set_language_layout.addWidget(self.language_combo)
        set_language_layout.addStretch()
        set_language_layout.addWidget(set_button)

        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        # main_layout.setSpacing(0) 
        main_layout.addWidget(title_label)
        # main_layout.addWidget(user_label)
        # main_layout.addStretch()
        main_layout.addLayout(set_language_layout)

        print(f'設定{title}畫面')

        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{title} Index: {self.stacked_widget.count()}')

    def setLanguage(self):
        PySQL.updateSQL_Var('language', PPV.get_keys_from_value(PPV.languages, self.language_combo.currentText())[0])
        print(f"設定語言為：{self.language_combo.currentText()}")