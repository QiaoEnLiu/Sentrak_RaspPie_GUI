#zh-tw 
# imgResource.py
# 此程式碼為按鈕及標籤取得圖示用的程式碼


from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QFontMetrics
from PyQt5.QtCore import Qt
from pkg_resources import resource_filename

stateAlarm_icons = {0:'Alarm icon null.jpg',
                    1:'Alarm 1 icon.jpg',
                    2:'Alarm 2 icon.jpg'}

stateWire_icons = {0:'RS485.png',
                   1:'Ethernet.png',
                   2:'usb icon.png'}

stateRecord_icons={0:'一次性紀錄.png',
                   1:'自動記錄.png',
                   2:'紀錄中.png',
                   3:'紀錄停止.png'}


stateInbMenu_icons = {0:'進入選單.png',
                      1:'settings icon.png',
                      2:'calibration icon.png',
                      3:'Identification icon.png',
                      4:'Data log icon.jpg'}

stateBattery_icons = {0:'Battery icon.png'}

stateBatteryCharge_icons = {0:'電量10以下.png',
                            1:'電量11-25.png',
                            2:'電量26-50.png',
                            3:'電量51-75.png',
                            4:'電量76-100.png',
                            5:'電量充電中.png'}

lock_icons = {0:'Lock icon.jpg',
              1:'Unlock icon.jpg'}



def setLabelIcon(label, image_path):
    image_path = resource_filename(__name__, 'picture/icon/'+image_path)
    pixmap = QPixmap(image_path)
    pixmap = pixmap.scaled(65, 65, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
    label.setPixmap(pixmap)

def setButtonIcon(button, image_path, text=""):
    # 使用 resource_filename 獲取圖片的路徑
    image_path = resource_filename(__name__, 'picture/icon/'+image_path)

    # 設置按鈕的圖片
    pixmap = QPixmap(image_path)

    # 獲取按鈕的大小
    button_size = button.size()

    # 使用 scaled 方法調整圖片大小以符合按鈕，同時保持原始的寬高比# 如果圖片尺寸超過 100x100，則進行調整
    if button.width() > 100 or button.height() > 100:
        # print('Image Set 1')
        pixmap = pixmap.scaled(button.width()//1.5, button.height()//1.5, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)


    else:
        # print('Image Set 2')
        pixmap = pixmap.scaled(button_size, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)

    # pixmap = pixmap.scaled(button_size, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
    # 設置按鈕的圖標
    icon = QIcon(pixmap)
    button.setIcon(icon)

    # 設置按鈕的圖標大小
    button.setIconSize(button_size)

    # button.setStyleSheet(button.styleSheet() + "QPushButton { text-align: bottom; }")

    # 將文字保存到按鈕的屬性中
    button.setProperty("text", text)
    # button.setStyleSheet("text-align: bottom")

    # 重新繪製按鈕
    # button.repaint()

# def paintEvent(button, event):
#     # super(QPushButton, self).paintEvent(event)
#     print('paintEvent called')

#     # 獲取按鈕的屬性中的文字
#     text = button.property("text")
    
#     if text:
#         print('Image Set 4')
#         # 繪製文字和圖片
#         painter = QPainter(button)
#         painter.setPen(Qt.black)
#         font_metrics = QFontMetrics(button.font())

#         # 獲取圖片的位置
#         pixmap_rect = button.icon().pixmap(button.iconSize()).rect()
#         pixmap_rect.moveTopLeft(button.rect().center() - pixmap_rect.center())  # 將圖片置於按鈕的上方並水平居中

#         # 計算文字的位置
#         text_rect = font_metrics.boundingRect(button.rect(), Qt.AlignCenter, text)
#         text_rect.moveTopLeft(QPoint(button.rect().center().x() - text_rect.width() / 2, pixmap_rect.bottom() + 5))  # 將文字置於圖片下方，上方留有 5 像素的空隙

#         # 繪製圖片和文字
#         button.icon().paint(painter, pixmap_rect.left(), pixmap_rect.top(), button.iconSize().width(), button.iconSize().height(), Qt.AlignLeft)
#         painter.drawText(text_rect, Qt.AlignCenter, text)

