from PyQt6.QtWidgets import QMessageBox, QDialog, QLineEdit, QVBoxLayout
from PyQt6 import QtGui
from UI.dlgChangePassword_ui import Ui_dlgChangePassword
#from UI.dlgChangePassword_ui import Ui_dlgChangePassword
from dbUtil import Database
from datetime import date, timedelta
from PyQt6.QtWidgets import QMessageBox

class ChangePassword(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_dlgChangePassword()
        self.ui.setupUi(self)
        #Setting tab order from OldPassword to NewPassword to VerifyPassword to Ok button
        self.setTabOrder(self.ui.txtOldPassword, self.ui.txtNewPassword)
        self.setTabOrder(self.ui.txtNewPassword, self.ui.txtVerifyPassword)
        self.setTabOrder(self.ui.txtVerifyPassword, self.ui.buttonBox) 
        self.ui.comboBoxUsername.setFocus() #Combobox gets initial focus
        self.ui.comboBoxUsername.activated.connect(self.ui.txtOldPassword.setFocus) #after combobox choice, oldpassword is focus
        self.ui.comboBoxUsername.setPlaceholderText("Select a username") #This won't be included in the list but will give helpful hint
        self.ui.comboBoxUsername.setCurrentIndex(-1)
        #load combobox with usernames
        db = Database('regular')
        allUsernames = db.fetchAllUsers()
        for name in allUsernames:
            self.ui.comboBoxUsername.addItem(name['username'])

    def accept(self):
        if (self.ui.txtOldPassword.text() and self.ui.txtNewPassword.text() and self.ui.txtVerifyPassword.text()):
            if (self.ui.txtNewPassword.text() == self.ui.txtVerifyPassword.text()):
                username = self.ui.comboBoxUsername.currentText()
                oldPassword = self.ui.txtOldPassword.text().encode('utf-8')
                newPassword = self.ui.txtNewPassword.text()
                db = Database('regular')
                storedPassword = db.readUserPassword(username)
                if (oldPassword == storedPassword):
                    db.writeNewUserPasswordToDB(username, newPassword)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Information)
                    msg.setText("Success writing new password for user " + username)
                    msg.setWindowTitle("Success changing password")
                    msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                    msg.exec()
                    self.done(1)
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Information)
                    msg.setText("Incorrect password!")
                    msg.setWindowTitle("Failure")
                    msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                    msg.exec()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText("New and Verify passwords don't match")
                msg.setWindowTitle("Failure")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                msg.exec()

    def revealPassword1(self):
        #print("clicked",self.ui.txtPassword.text())
        if (self.ui.txtOldPassword.text()):
            if (self.ui.txtOldPassword.echoMode() == QLineEdit.EchoMode.Password):
                self.ui.txtOldPassword.setEchoMode(QLineEdit.EchoMode.Normal)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("d:\\Code\\python\\searcher\\UI\\images/eye-open.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                self.ui.btnEyeOldPassword.setIcon(icon)
            else:
                self.ui.txtOldPassword.setEchoMode(QLineEdit.EchoMode.Password)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("d:\\Code\\python\\searcher\\UI\\images/eye-close.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                self.ui.btnEyeOldPassword.setIcon(icon)

    def revealPassword2(self):     
        if (self.ui.txtNewPassword.text()):
            if (self.ui.txtNewPassword.echoMode() == QLineEdit.EchoMode.Password):
                self.ui.txtNewPassword.setEchoMode(QLineEdit.EchoMode.Normal)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("d:\\Code\\python\\searcher\\UI\\images/eye-open.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                self.ui.btnEyeNewPassword.setIcon(icon)
            else:
                self.ui.txtNewPassword.setEchoMode(QLineEdit.EchoMode.Password)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("d:\\Code\\python\\searcher\\UI\\images/eye-close.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                self.ui.btnEyeNewPassword.setIcon(icon)

    def revealPassword3(self):     
        if (self.ui.txtVerifyPassword.text()):
            if (self.ui.txtVerifyPassword.echoMode() == QLineEdit.EchoMode.Password):
                self.ui.txtVerifyPassword.setEchoMode(QLineEdit.EchoMode.Normal)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("d:\\Code\\python\\searcher\\UI\\images/eye-open.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                self.ui.btnEyeVerifyPassword.setIcon(icon)
            else:
                self.ui.txtVerifyPassword.setEchoMode(QLineEdit.EchoMode.Password)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("d:\\Code\\python\\searcher\\UI\\images/eye-close.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                self.ui.btnEyeVerifyPassword.setIcon(icon)