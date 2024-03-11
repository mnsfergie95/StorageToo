import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QWidget, QTableWidgetItem
from PyQt6.QtCore import QFile, Qt
from PyQt6 import QtCore
from UI.MainWindow_ui import Ui_MainWindow
from UI.dlgLogin_ui import Ui_Dialog
from dbUtil import Database
#from filename import classname
import re # regular expression
from datetime import datetime
import calendar
from LesseeDAO import LesseeDAO
from Crypto.Cipher import AES
from Payment import Payment

class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def closeEvent(self, event):
        sys.exit(0)

    def checkCredentials(self):
        if (self.ui.txtUsername.text() == "admin"):
            obj = AES.new('This is a key123'.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))
            #hidden = bytes('Hawaii2022!*****'.encode("utf8"))
            with open('users.txt', 'rb') as f:
                hidden = f.read(16)
            secret = obj.decrypt(hidden)
            inputted = bytes(self.ui.txtPassword.text().ljust(16,'*').encode("utf8")) #user input padded to 16 bytes with * on the right
            if (inputted == secret):
                self.done(1) #0=rejected, 1=accepted

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def populateCmbAvailUnits(self):
        window.ui.cmbUnitsAvail.addItem("Select a unit")
        db = Database()
        list = db.populateList_AvailUnits()
        for name in list:
            window.ui.cmbUnitsAvail.addItem(name['label'])
                
    def populateCmbLeasedUnits(self):
        window.ui.cmbUnitsLeased.addItem("Select a unit")
        db = Database()
        list = db.populateList_LeasedUnits()
        for name in list:
            window.ui.cmbUnitsLeased.addItem(name['label'])

    def clearResultArea(self):
        self.ui.textBrowserResult.setText("")

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

    ''' search for lessee using unit, name, or phone '''
    def searchLessee(self):
        if not(window.ui.cmbUnitsLeased.currentText() == "Select a unit"):
            unit = window.ui.cmbUnitsLeased.currentText()
        else: 
            unit = ""
        name = window.ui.txtNameSearch.text()
        print("name sent to dbUtil is ",name)
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
            
    def showAllLessees(self):
        window.ui.tableWidget.setRowCount(0)
        lessees = LesseeDAO.populateLessees()
        #print("lessees is ", lessees)
        for lessee in lessees:
            self.populateTableRow(lessee)
        

    ''' Add a lessee to DB '''
    def insertLessee(self):
        # check for minimum data entry requirement...name,unit, and phone
        label = window.ui.cmbUnitsAvail.currentText()
        name = window.ui.txtName.text()
        phone = window.ui.txtPhone.text()
        window.ui.textBrowserResult.setText("")
        if ((label != "Select a unit") and (name != "") and (phone != "")):
            #check phone input and format it (###) ###-####
            valid = re.compile(r"^((\(\d{3}\))|\d{3})[- .]?\d{3}[- .]?\d{4}$")
            if (not valid.match(phone)):
                window.ui.textBrowserResult.setText("Invalid phone number entered.\nMust be ten digits  or be of this format: (###) ###-####.  Please fix.")
                return
            formattedPhone = re.sub(r'(\d{3})(\d{3})(\d{4})', r'(\1) \2-\3', phone)
            #check user input for zip
            zip = 0
            zipStr = window.ui.txtZip.text()
            if (len(zipStr) == 5):
                try:
                    zip = int(zipStr)
                except:
                    window.ui.textBrowserResult.setText("Invalid zipcode entered.  Please fix.")
                    return
            else:
                window.ui.textBrowserResult.setText("Invalid zipcode entered.  Please fix.")
                return
            #calculate partial pmt
            input_dt = datetime.now()
            res = calendar.monthrange(input_dt.year, input_dt.month) #Return weekday (0-6 ~ Mon-Sun) and number of days (28-31) for year, month.
            LastDayOfMonth = res[1]
            TodayDayOfMonth = input_dt.day
            DaysLeftInMonth = LastDayOfMonth - TodayDayOfMonth
            monthlyPrice = float(LesseeDAO.getMonthlyAmt(label)['monthly_price'])
            partialPayment = round(monthlyPrice * DaysLeftInMonth / LastDayOfMonth, 2)  
            firstOfThisMonth = input_dt.replace(day=1)
            firstNextMonth = self.add_months(firstOfThisMonth, 1)
            #popup a dialog showing partial payment amt
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Hello!")
            dlg.setText("Partial payment is " + str(partialPayment))
            dlg.exec()
            #insert partial payment and lessee into db
            args = (label, label, partialPayment, input_dt, firstNextMonth, name, window.ui.txtAddrL1.text(), window.ui.txtAddrL2.text(),
                    window.ui.txtCity.text(), window.ui.txtState.text(), zip, formattedPhone)
            print(args)
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
        dlgPmt.populateCmbLeasedUnits()
        dlgPmt.exec()
                    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    '''
    dlgLogin = Dialog()
    dlgLogin.setWindowTitle("Login")
    dlgLogin.ui.txtUsername.setFocus()
    dlgLogin.ui.txtUsername.editingFinished.connect(dlgLogin.ui.txtPassword.setFocus)
    dlgLogin.ui.btnLogin.clicked.connect(dlgLogin.checkCredentials)
    dlgLogin.exec()
    '''

    window = MainWindow()
    window.ui.btnAddLessee.clicked.connect(window.insertLessee)
    window.ui.btnSearchLessee.clicked.connect(window.searchLessee)
    window.ui.btnDisplayAllLessees.clicked.connect(window.showAllLessees)
    window.ui.btnLamda.clicked.connect(window.lamda)
    window.ui.btnPayment.clicked.connect(window.payment)
    window.populateCmbAvailUnits()
    window.populateCmbLeasedUnits()
    window.show()

    sys.exit(app.exec())

    