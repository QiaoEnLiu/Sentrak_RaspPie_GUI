#zh-tw
# testEndFrame.py

# 此程式碼為子畫面最終刷新測試碼
    # 尚未實作的功能介面都會先以此介面顯示
try:
    import traceback, csv
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
    from PyQt5.QtGui import QFont

    import ProjectPublicVariable as PPV
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()

filename = 'Sentrak'
fileContentTitle=['名稱','裝置','介面','橋接']
fileContentList=[filename,'RaspPie','PyQt5','modbusRTU']
fileContent = [fileContentTitle, fileContentList]
data_text = '\n'.join([','.join(row) for row in fileContent])

class recordDownloadFileFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages, mainTitle):
        super().__init__()
        print(title)

        self.sub_pages=sub_pages
        
        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(32)
        title_label.setFont(font)
        # title_label.setStyleSheet(_style)

        
        file_label = QLabel(f'檔案名稱：{filename}\n檔案內容：\n{data_text}')
        font.setPointSize(16)
        file_label.setFont(font)

        recordDownload = QPushButton('下載檔案')
        font.setPointSize(24)
        recordDownload.setFont(font)

        
        # user_label = QLabel(PPV.presentUser.userInfo())
        # user_label.setFont(font)
        # user_label.setStyleSheet(_style)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0) 
        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)
        file_layout = QVBoxLayout()
        file_layout.addWidget(file_label)
        download_layout = QVBoxLayout()
        download_layout.addWidget(recordDownload)
        main_layout.addLayout(title_layout)
        main_layout.addLayout(file_layout)
        main_layout.addLayout(download_layout)
        # main_layout.addWidget(user_label)

        # print('終節點測試畫面：', title)

        recordDownload.clicked.connect(self.downloadFile)

        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print(f'{title} Index: {self.stacked_widget.count()}')

    def downloadFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "儲存 CSV 檔案", filename+".csv", "CSV 檔案 (*.csv);;All Files (*)", options=options)

        if file_name:
            # 這裡可以修改或產生 CSV 資料，以下是一個簡單的範例
            data = fileContent
            with open(file_name, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerows(data)