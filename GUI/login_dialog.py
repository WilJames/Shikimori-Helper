# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(148, 180)
        Dialog.setMaximumSize(QtCore.QSize(16777215, 180))
        Dialog.setSizeGripEnabled(False)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setChecked(False)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout.addWidget(self.checkBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 1)
        self.label_password = QtWidgets.QLabel(Dialog)
        self.label_password.setObjectName("label_password")
        self.gridLayout.addWidget(self.label_password, 2, 0, 1, 1)
        self.lineEdit_login = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_login.setObjectName("lineEdit_login")
        self.gridLayout.addWidget(self.lineEdit_login, 1, 0, 1, 1)
        self.label_login = QtWidgets.QLabel(Dialog)
        self.label_login.setObjectName("label_login")
        self.gridLayout.addWidget(self.label_login, 0, 0, 1, 1)
        self.label_inform = QtWidgets.QLabel(Dialog)
        self.label_inform.setBaseSize(QtCore.QSize(0, 0))
        self.label_inform.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_inform.setText("")
        self.label_inform.setObjectName("label_inform")
        self.gridLayout.addWidget(self.label_inform, 7, 0, 1, 1)
        self.lineEdit_password = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_password.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.gridLayout.addWidget(self.lineEdit_password, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pushButton_enter = QtWidgets.QPushButton(Dialog)
        self.pushButton_enter.setObjectName("pushButton_enter")
        self.horizontalLayout_2.addWidget(self.pushButton_enter)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", " "))
        self.checkBox.setText(_translate("Dialog", "Запомнить"))
        self.label_password.setText(_translate("Dialog", "Пароль:"))
        self.label_login.setText(_translate("Dialog", "Логин:"))
        self.pushButton_enter.setText(_translate("Dialog", "Вход"))


