# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\AnacodaProject\Sentrak_RaspPie_GUI\ui\manu_page(Widget).ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_menu_page_widget(object):
    def setupUi(self, menu_page_widget):
        menu_page_widget.setObjectName("menu_page_widget")
        menu_page_widget.resize(400, 360)
        menu_page_widget.setMinimumSize(QtCore.QSize(400, 360))
        menu_page_widget.setMaximumSize(QtCore.QSize(400, 360))
        menu_page_widget.setSizeIncrement(QtCore.QSize(400, 360))
        menu_page_widget.setBaseSize(QtCore.QSize(400, 360))
        self.menu_page = QtWidgets.QFrame(menu_page_widget)
        self.menu_page.setGeometry(QtCore.QRect(0, 0, 400, 360))
        self.menu_page.setMaximumSize(QtCore.QSize(400, 360))
        self.menu_page.setSizeIncrement(QtCore.QSize(400, 360))
        self.menu_page.setBaseSize(QtCore.QSize(400, 360))
        self.menu_page.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.menu_page.setFrameShadow(QtWidgets.QFrame.Raised)
        self.menu_page.setObjectName("menu_page")
        self.gridLayoutWidget = QtWidgets.QWidget(self.menu_page)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 401, 361))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.menu_page_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.menu_page_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.menu_page_layout.setContentsMargins(0, 0, 0, 0)
        self.menu_page_layout.setSpacing(0)
        self.menu_page_layout.setObjectName("menu_page_layout")
        self.set_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.set_button.setMinimumSize(QtCore.QSize(125, 125))
        self.set_button.setMaximumSize(QtCore.QSize(125, 125))
        self.set_button.setSizeIncrement(QtCore.QSize(125, 125))
        self.set_button.setBaseSize(QtCore.QSize(125, 125))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.set_button.setFont(font)
        self.set_button.setObjectName("set_button")
        self.menu_page_layout.addWidget(self.set_button, 0, 0, 1, 1)
        self.record_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.record_button.setMinimumSize(QtCore.QSize(125, 125))
        self.record_button.setMaximumSize(QtCore.QSize(125, 125))
        self.record_button.setSizeIncrement(QtCore.QSize(125, 125))
        self.record_button.setBaseSize(QtCore.QSize(125, 125))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.record_button.setFont(font)
        self.record_button.setObjectName("record_button")
        self.menu_page_layout.addWidget(self.record_button, 1, 0, 1, 1)
        self.calibrate_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.calibrate_button.setMinimumSize(QtCore.QSize(125, 125))
        self.calibrate_button.setMaximumSize(QtCore.QSize(125, 125))
        self.calibrate_button.setSizeIncrement(QtCore.QSize(125, 125))
        self.calibrate_button.setBaseSize(QtCore.QSize(125, 125))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.calibrate_button.setFont(font)
        self.calibrate_button.setObjectName("calibrate_button")
        self.menu_page_layout.addWidget(self.calibrate_button, 0, 1, 1, 1)
        self.identify_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.identify_button.setMinimumSize(QtCore.QSize(125, 125))
        self.identify_button.setMaximumSize(QtCore.QSize(125, 125))
        self.identify_button.setSizeIncrement(QtCore.QSize(125, 125))
        self.identify_button.setBaseSize(QtCore.QSize(125, 125))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.identify_button.setFont(font)
        self.identify_button.setObjectName("identify_button")
        self.menu_page_layout.addWidget(self.identify_button, 1, 1, 1, 1)

        self.retranslateUi(menu_page_widget)
        QtCore.QMetaObject.connectSlotsByName(menu_page_widget)

    def retranslateUi(self, menu_page_widget):
        _translate = QtCore.QCoreApplication.translate
        menu_page_widget.setWindowTitle(_translate("menu_page_widget", "Form"))
        self.set_button.setText(_translate("menu_page_widget", "設定"))
        self.record_button.setText(_translate("menu_page_widget", "記錄"))
        self.calibrate_button.setText(_translate("menu_page_widget", "校正"))
        self.identify_button.setText(_translate("menu_page_widget", "識別"))
