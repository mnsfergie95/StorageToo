# Form implementation generated from reading ui file 'd:\Code\python\searcher\UI\dlgLogin.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(140, 140, 251, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnLogin = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnLogin.setFont(font)
        self.btnLogin.setObjectName("btnLogin")
        self.horizontalLayout.addWidget(self.btnLogin)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayoutWidget = QtWidgets.QWidget(parent=Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(70, 30, 261, 101))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.txtPassword = QtWidgets.QLineEdit(parent=self.gridLayoutWidget)
        self.txtPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.txtPassword.setObjectName("txtPassword")
        self.gridLayout.addWidget(self.txtPassword, 1, 1, 1, 1)
        self.txtUsername = QtWidgets.QLineEdit(parent=self.gridLayoutWidget)
        self.txtUsername.setObjectName("txtUsername")
        self.gridLayout.addWidget(self.txtUsername, 0, 1, 1, 1)
        self.lblUsername = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lblUsername.setFont(font)
        self.lblUsername.setObjectName("lblUsername")
        self.gridLayout.addWidget(self.lblUsername, 0, 0, 1, 1)
        self.lblPassword = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lblPassword.setFont(font)
        self.lblPassword.setObjectName("lblPassword")
        self.gridLayout.addWidget(self.lblPassword, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btnLogin.setText(_translate("Dialog", "Login -->"))
        self.lblUsername.setText(_translate("Dialog", "Username:"))
        self.lblPassword.setText(_translate("Dialog", "Password:"))
