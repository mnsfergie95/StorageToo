from PyQt6.QtWidgets import QMessageBox, QDialog, QLineEdit
from PyQt6 import QtGui
from UI.dlgAddUser_ui import Ui_dlgAddUser
from dbUtil import Database
#from PaymentDAO import PaymentDAO
from datetime import date, timedelta
from PyQt6.QtWidgets import QMessageBox

class AddUser(QDialog):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_dlgAddUser()
        self.ui.setupUi(self)
        self.ui.txtUsername.setFocus()

    def accept(self):
        #print("username is ", self.ui.txtUsername.text())
        #print("password is ", self.ui.txtPassword.text())
        username = self.ui.txtUsername.text()
        password = self.ui.txtPassword.text()
        db = Database('admin')
        if (db.writeNewUserToDB(username)):
            db.writeNewUserPasswordToDB(username, password)
        else:
            print("username already exists")
        return super().accept()
    
    def revealPassword(self):
        #print("clicked",self.ui.txtPassword.text())
        if (self.ui.txtPassword.text()):
            if (self.ui.txtPassword.echoMode() == QLineEdit.EchoMode.Password):
                self.ui.txtPassword.setEchoMode(QLineEdit.EchoMode.Normal)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("d:\\Code\\python\\searcher\\UI\\images/eye-open.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                self.ui.btnEye.setIcon(icon)
            else:
                self.ui.txtPassword.setEchoMode(QLineEdit.EchoMode.Password)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("d:\\Code\\python\\searcher\\UI\\images/eye-close.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                self.ui.btnEye.setIcon(icon)
