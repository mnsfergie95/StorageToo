import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QLineEdit, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QFile, Qt
from PyQt6 import QtCore, QtGui
from UI.MainWindow_ui import Ui_MainWindow
from UI.dlgLogin_ui import Ui_dlgLogin
from Admin import Admin
from dbUtil import Database
#from filename import classname
import re # regular expression
from datetime import datetime
import calendar
from LesseeDAO import LesseeDAO
from Crypto.Cipher import AES
from Payment import Payment
from us_state_abbrev import us_state_to_abbrev
from decimal import Decimal, ROUND_HALF_UP

class dlgLogin(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_dlgLogin()
        self.ui.setupUi(self)
        
    def closeEvent(self, event):
        sys.exit(0)

    def callAdmin(self):
        dlgAdmin = Admin()
        dlgAdmin.setWindowTitle("Administrator")
        dlgAdmin.ui.btnAddUser.clicked.connect(dlgAdmin.addNewUser)
        dlgAdmin.ui.btnChangePassword.clicked.connect(dlgAdmin.changePassword)
        dlgAdmin.exec()

    def credentialsFail(self, msgText):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(msgText)
        msg.setWindowTitle("Failure")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msg.exec()

    def checkCredentials(self):
        username = self.ui.txtUsername.text()
        password = self.ui.txtPassword.text()
        if (username and password):
            db = Database('regular')
            if (db.isUserInDB(username)):
                storedPassword = db.readUserPassword(username)
                enteredPassword = self.ui.txtPassword.text().encode('utf-8')
                if (storedPassword == enteredPassword):
                    if (username == "admin"):
                        self.callAdmin()
                    else:
                        self.done(1)
                else:
                    self.credentialsFail("Username and/or password incorrect")
                    self.ui.txtUsername.clear()
                    self.ui.txtPassword.clear()
                    self.ui.txtUsername.setFocus()
            else:
                self.credentialsFail("Username and/or password incorrect")
                self.ui.txtUsername.clear()
                self.ui.txtPassword.clear()
                self.ui.txtUsername.setFocus()
        else:
            self.credentialsFail("Must enter a username and password!")

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

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.setColumnWidth(0,35) #unit
        self.ui.tableWidget.setColumnWidth(1,150) #name
        self.ui.tableWidget.setColumnWidth(2,140) #phone
        self.ui.tableWidget.setColumnWidth(3,130) #addr Line 1
        self.ui.tableWidget.setColumnWidth(4,80) #addr Line 2
        self.ui.tableWidget.setColumnWidth(6,35) #state
        self.ui.tableWidget.setSortingEnabled(True) #allow sorting by clicking on any column header

    ''' combo box available units (where 'active' = 0) '''
    def populateCmbAvailUnits(self):
        self.ui.cmbUnitsAvail.setPlaceholderText("Select a unit") #This won't be included in the list but will give helpful hint
        self.ui.cmbUnitsAvail.setCurrentIndex(-1)
        #window.ui.cmbUnitsAvail.addItem("Select a unit")
        db = Database('regular')
        list = db.populateList_AvailUnits()
        for name in list:
            window.ui.cmbUnitsAvail.addItem(name['label'])
                
    ''' combo box Leased Units (where 'active' = 1) '''                 
    def populateCmbLeasedUnits(self):
        self.ui.cmbUnitsLeased.setPlaceholderText("Select a unit") #This won't be included in the list but will give helpful hint
        self.ui.cmbUnitsLeased.setCurrentIndex(-1)
        #window.ui.cmbUnitsLeased.addItem("Select a unit")
        db = Database('regular')
        list = db.populateList_LeasedUnits()
        for name in list:
            window.ui.cmbUnitsLeased.addItem(name['label'])

    def clearResultArea(self):
        self.ui.textBrowserResult.setText("")

    ''' add months to current date to generate next payment date '''
    def add_months(self, current_date, months_to_add):
        new_date = datetime(current_date.year + (current_date.month + months_to_add - 1) // 12,
                        (current_date.month + months_to_add - 1) % 12 + 1,
                        current_date.day, current_date.hour, current_date.minute, current_date.second)
        return new_date
    
    def populateTableRow(self, lessor):
        for rowNumber, rowData in enumerate(lessor):
            window.ui.tableWidget.insertRow(rowNumber)
            window.ui.tableWidget.setItem(rowNumber, 0, QTableWidgetItem(rowData['label']))
            window.ui.tableWidget.setItem(rowNumber, 1, QTableWidgetItem(rowData['lesseename']))
            window.ui.tableWidget.setItem(rowNumber, 2, QTableWidgetItem(rowData['phone']))
            window.ui.tableWidget.setItem(rowNumber, 3, QTableWidgetItem(rowData['addrl1']))
            window.ui.tableWidget.setItem(rowNumber, 4, QTableWidgetItem(rowData['addrl2']))
            window.ui.tableWidget.setItem(rowNumber, 5, QTableWidgetItem(rowData['city']))
            window.ui.tableWidget.setItem(rowNumber, 6, QTableWidgetItem(rowData['state']))
            window.ui.tableWidget.setItem(rowNumber, 7, QTableWidgetItem(str(rowData['zip'])))
            is_active = rowData['active'] == 1
            window.ui.tableWidget.setItem(rowNumber, 8, QTableWidgetItem(str(is_active)))

    ''' search for lessee using unit, name, or phone '''
    def searchLessee(self):
        if not(self.ui.cmbUnitsLeased.currentIndex == -1):
            unit = window.ui.cmbUnitsLeased.currentText()
        else: 
            unit = ""
        name = window.ui.txtNameSearch.text()
        phone = window.ui.txtPhone.text()
        formattedPhone = ""
        if (phone != ""):
            #check phone input and format it (###) ###-####
            valid = re.compile(r"^((\(\d{3}\))|\d{3})[- .]?\d{3}[- .]?\d{4}$")
            if (not valid.match(phone)):
                window.ui.textBrowserResult.setText("Invalid phone number entered.\nMust be ten digits  or be of this format: (###) ###-####.  Please fix.")
                return
            formattedPhone = re.sub(r'(\d{3})(\d{3})(\d{4})', r'(\1) \2-\3', phone)
        lessor = LesseeDAO.searchLessee(name, unit, formattedPhone)
        window.ui.tableWidget.setRowCount(0)
        self.populateTableRow(lessor)
            
    ''' show all lessees (current) '''
    def showAllCurrentLessees(self):
        window.ui.tableWidget.setRowCount(0)
        lessees = LesseeDAO.populateCurrentLessees()
        for lessee in lessees:
            self.populateTableRow(lessee)
        
    ''' show all lessees (former) '''
    def showAllFormerLessees(self):
        window.ui.tableWidget.setRowCount(0)
        lessees = LesseeDAO.populateFormerLessees()
        for lessee in lessees:
            self.populateTableRow(lessee)    

    ''' Add a lessee to DB '''
    def insertLessee(self):
        # check for minimum data entry requirement...name,unit, and phone
        label = ""
        if self.ui.cmbUnitsAvail.currentIndex == -1:
            label = "default"
        else:
            label = window.ui.cmbUnitsAvail.currentText()
        name = window.ui.txtName.text()
        phone = window.ui.txtPhone.text()
        window.ui.textBrowserResult.setText("")
        if ((label != "default") and (name != "") and (phone != "")):
            #check phone input and format it (###) ###-####
            valid = re.compile(r"^((\(\d{3}\))|\d{3})[- .]?\d{3}[- .]?\d{4}$")
            if (not valid.match(phone)):
                window.ui.textBrowserResult.setText("Invalid phone number entered.\nMust be ten digits  or be of this format: (###) ###-####.  Please fix.")
                return
            formattedPhone = re.sub(r'(\d{3})(\d{3})(\d{4})', r'(\1) \2-\3', phone)
            #check user input for zip
            zipStr = window.ui.txtZip.text()
            if zipStr != "":
                #Validates a US ZIP code (5-digit or ZIP+4 format) using regex.
                pattern = r"^\d{5}(?:-\d{4})?$"
                if not (re.match(pattern, zipStr)):
                    window.ui.textBrowserResult.setText("Invalid zipcode entered.  Please fix.")
                    return
            #validate state user input
            try:
                stateInput = window.ui.txtState.text().title()
                stateAbbrev = us_state_to_abbrev[stateInput]
            except KeyError as e:
                msg = "incorrect state input"
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Oops!")
                dlg.setText(msg)
                dlg.exec()
                return
            #calculate partial pmt
            input_dt = datetime.now()
            res = calendar.monthrange(input_dt.year, input_dt.month) #Return weekday (0-6 ~ Mon-Sun) and number of days (28-31) for year, month.
            LastDayOfMonth = res[1]
            TodayDayOfMonth = input_dt.day
            DaysLeftInMonth = LastDayOfMonth - TodayDayOfMonth
            monthlyPrice = float(LesseeDAO.getMonthlyAmt(label)['monthly_price'])
            amountPartial = Decimal(monthlyPrice * DaysLeftInMonth / LastDayOfMonth)
            partialPayment =  amountPartial.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) 
            firstOfThisMonth = input_dt.replace(day=1)
            firstNextMonth = self.add_months(firstOfThisMonth, 1).date()
            #popup a dialog showing partial payment amt
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Hello!")
            dlg.setText("Partial payment is " + str(partialPayment))
            dlg.exec()
            #insert partial payment and lessee into db
            args = (label, partialPayment, input_dt, firstNextMonth, name, window.ui.txtAddrL1.text(), window.ui.txtAddrL2.text(),
                    window.ui.txtCity.text(), stateAbbrev, zipStr, formattedPhone)
            LesseeDAO.insertLessee(*args)
            #clear the form values
            window.ui.cmbUnitsAvail.removeItem(window.ui.cmbUnitsAvail.currentIndex())
            window.ui.txtName.setText("")
            window.ui.txtAddrL1.setText("")
            window.ui.txtAddrL2.setText("")
            window.ui.txtCity.setText("")
            window.ui.txtState.setText("")
            window.ui.txtZip.setText("")
            window.ui.txtPhone.setText("")
            #set result area to lessee successfully added to DB!
            window.ui.textBrowserResult.setText("Lessee successfully added to DB!")
        else:
            window.ui.textBrowserResult.setText("A unit must be chosen, a name entered, and a phone number entered")

    def lamda(self):
        mult = lambda x, y : x * y
        window.ui.textBrowserResult.setText("mult is " + str(mult(4,7)))

    def payment(self):
        dlgPmt = Payment()
        dlgPmt.ui.btnAmtOwed.clicked.connect(dlgPmt.showAmtOwed)
        dlgPmt.ui.btnRecvPmt.clicked.connect(dlgPmt.recvPmt)
        dlgPmt.ui.btnPmtHistory.clicked.connect(dlgPmt.showPmtHistory)
        dlgPmt.ui.btnInvoice.clicked.connect(dlgPmt.printInvoice)
        dlgPmt.populateCmbLeasedUnits()
        dlgPmt.exec()
                    
if __name__ == "__main__":
    app = QApplication(sys.argv)
       
    dialogLogin = dlgLogin()
    dialogLogin.setWindowTitle("Login")
    dialogLogin.ui.txtUsername.setFocus()
    dialogLogin.ui.txtUsername.editingFinished.connect(dialogLogin.ui.txtPassword.setFocus)
    dialogLogin.ui.btnLogin.clicked.connect(dialogLogin.checkCredentials)
    dialogLogin.ui.btnEye.clicked.connect(dialogLogin.revealPassword)
    dialogLogin.exec()
    
    window = MainWindow()
    window.ui.btnAddLessee.clicked.connect(window.insertLessee)
    window.ui.btnSearchLessee.clicked.connect(window.searchLessee)
    window.ui.btnDisplayCurrentLessees.clicked.connect(window.showAllCurrentLessees)
    window.ui.btnDisplayFormerLessees.clicked.connect(window.showAllFormerLessees)
    window.ui.btnLamda.clicked.connect(window.lamda)
    window.ui.btnPayment.clicked.connect(window.payment)
    window.populateCmbAvailUnits()
    window.populateCmbLeasedUnits()
    window.show()
    
    sys.exit(app.exec())

    