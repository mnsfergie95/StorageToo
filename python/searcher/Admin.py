from PyQt6.QtWidgets import QMessageBox, QDialog
from UI.dlgAdmin_ui import Ui_dlgAdmin
from dbUtil import Database
#from PaymentDAO import PaymentDAO
from datetime import date, timedelta
from PyQt6.QtWidgets import QMessageBox
from AddUser import AddUser
from ChangePassword import ChangePassword

class Admin(QDialog):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_dlgAdmin()
        self.ui.setupUi(self)
        self.ui.btnAddUser.setFocus()

    def closeEvent(self, event):
        self.done(1)

    def addNewUser(self):
        dlgAddUser = AddUser()
        dlgAddUser.setWindowTitle("Add new user")
        dlgAddUser.ui.btnEye.clicked.connect(dlgAddUser.revealPassword)
        dlgAddUser.exec()

    def changePassword(self):
        dlgChangePassword = ChangePassword()
        dlgChangePassword.setWindowTitle("Change Password")
        dlgChangePassword.ui.btnEyeOldPassword.clicked.connect(dlgChangePassword.revealPassword1)
        dlgChangePassword.ui.btnEyeNewPassword.clicked.connect(dlgChangePassword.revealPassword2)
        dlgChangePassword.ui.btnEyeVerifyPassword.clicked.connect(dlgChangePassword.revealPassword3)
        dlgChangePassword.exec()

    

    
                
    

    
                
                
                
            
        
        

       
    