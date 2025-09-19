from PyQt6.QtWidgets import QMessageBox, QDialog
from UI.dlgPayment_ui import Ui_dlgPayment
from dbUtil import Database
from PaymentDAO import PaymentDAO
from datetime import date, timedelta
from PyQt6.QtWidgets import QMessageBox
import generatePDF

class Payment(QDialog):
    lateAmount = float(0.0)
    daysLate = 0
    monthlyAmt = float(0.0)
    current_date = date.today()
    nextDueDate = date(current_date.year + (current_date.month) // 12,
                        (current_date.month) % 12 + 1,
                        1)

    def __init__(self):
        super().__init__()
        self.ui = Ui_dlgPayment()
        self.ui.setupUi(self)
        print("nextDueDate is ", self.nextDueDate)

    def populateCmbLeasedUnits(self):
        self.ui.cmbLeasedUnits.setPlaceholderText("Select a unit") #This won't be included in the list but will give helpful hint
        self.ui.cmbLeasedUnits.setCurrentIndex(-1)
        #self.ui.cmbLeasedUnits.addItem("Select a unit")
        db = Database('regular')
        list = db.populateList_LeasedUnits()
        for name in list:
            self.ui.cmbLeasedUnits.addItem(name['label'])

    def add_month(self, current_date):
        # // rounds down, so only when month equals 12 does answer = 1
        # % is remainder so when month equals 12, 12/12 = 1 remainder 0 then + 1 = 1
        new_date = date(current_date.year + (current_date.month) // 12,
                        (current_date.month) % 12 + 1,
                        current_date.day)
        return new_date

    def getAmtOwed(self):
        self.lateAmount = 0.0
        self.monthlyAmt = 0.0
        whichUnitString = self.ui.cmbLeasedUnits.currentText()
        if not(self.ui.cmbLeasedUnits.currentIndex() == -1):
            pmt = PaymentDAO.getLastPayment(whichUnitString)
            late = PaymentDAO.getLateFees()
            self.lateAmount = 0.0
            self.daysLate = 0
            monthlyPrice = PaymentDAO.getMonthlyAmt(whichUnitString)
            self.monthlyAmt = monthlyPrice['monthly_price']
            currentDueDate = pmt[0]['NextDueDate']
            self.nextDueDate = self.add_month(currentDueDate)
            todayDate = date.today()
            howLate = (todayDate - currentDueDate).days
            match howLate:
                case howLate if howLate > 45:
                    self.daysLate = 45
                    for row in late:
                        if row['daysLate'] == 45:
                            self.lateAmount = row['lateFee']
                case howLate if howLate > 30:
                    self.daysLate = 30
                    for row in late:
                        if row['daysLate'] == 30:
                            self.lateAmount = row['lateFee']
                case howLate if howLate > 15:
                    self.daysLate = 15
                    for row in late:
                        if row['daysLate'] == 15:
                            self.lateAmount = row['lateFee']           

    def showAmtOwed(self):
        if not(self.ui.cmbLeasedUnits.currentIndex() == -1):
            self.getAmtOwed()
            totalAmtOwed = float(self.monthlyAmt) + self.lateAmount
            self.ui.textBrowser.setText("Monthly Amt $"+str(self.monthlyAmt)+"\nLate Fee $"+str(self.lateAmount)+"\nTotal $"+str(totalAmtOwed))
        else:
            self.ui.textBrowser.setText("Must select a unit")
                
    def recvPmt(self):
        #if unit selected then run showAmtOwed
        whichUnitString = self.ui.cmbLeasedUnits.currentText()
        if not(self.ui.cmbLeasedUnits.currentIndex() == -1):
            self.showAmtOwed()
            #commit payment to db
            amtOwed = self.monthlyAmt + self.lateAmount
            todayDate = date.today()
            PaymentDAO.commitPmt(whichUnitString, amtOwed, todayDate, self.nextDueDate)
            #popup a dialog showing successful addition to db
            msgBox = QMessageBox()
            msgBox.setText("Payment successfully added to db!")
            msgBox.exec()
            self.ui.textBrowser.setText("")
        else:
            self.ui.textBrowser.setText("Must select a unit!")

    def showPmtHistory(self):
        whichUnitString = self.ui.cmbLeasedUnits.currentText()
        PaymentDAO.getPayments(whichUnitString)
        print("show payments...")
        pass

    def printInvoice(self):
        whichUnitString = self.ui.cmbLeasedUnits.currentText()       
        '''
        call getAmtOwed  return dueDate also      
        getLesseeName from db
        call makePDF(lesseename, whichUnitString, amtOwed, dueDate)
        '''        
            
        
        

       

    
