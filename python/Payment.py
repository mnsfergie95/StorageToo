from PyQt6.QtWidgets import QMessageBox, QDialog
from UI.dlgPayment_ui import Ui_dlgPayment
from dbUtil import Database
from PaymentDAO import PaymentDAO
from datetime import date, timedelta
from PyQt6.QtWidgets import QMessageBox

class Payment(QDialog):
    lateAmount = 0.0
    daysLate = 0
    monthlyAmt = 0.0
    nextDueDate = date(2020, 12, 1)

    def __init__(self):
        super().__init__()
        self.ui = Ui_dlgPayment()
        self.ui.setupUi(self)

    def populateCmbLeasedUnits(self):
        self.ui.cmbLeasedUnits.addItem("Select a unit")
        db = Database()
        list = db.populateList_LeasedUnits()
        for name in list:
            self.ui.cmbLeasedUnits.addItem(name['label'])

    def add_month(self, current_date):
        new_date = date(current_date.year + (current_date.month) // 12,
                        (current_date.month) % 12 + 1,
                        current_date.day)
        return new_date

    def showAmtOwed(self):
        whichUnitString = self.ui.cmbLeasedUnits.currentText()
        if not(whichUnitString == "Select a unit"):
            pmt = PaymentDAO.getLastPayment(whichUnitString)
            late = PaymentDAO.getLateFees()
            #print(late)
            #return
            if (pmt != None):
                self.lateAmount = 0.0
                self.daysLate = 0
                monthlyPrice = PaymentDAO.getMonthlyAmt(whichUnitString)
                self.monthlyAmt = monthlyPrice['monthly_price']
                currentDueDate = pmt[0]['NextDueDate']
                self.nextDueDate = self.add_month(currentDueDate)
                todayDate = date.today()
                howLate = (todayDate - currentDueDate).days
                if (howLate > 45):
                    self.daysLate = 45
                    for row in late:
                        if row['daysLate'] == 45:
                            self.lateAmount = row['lateFee']
                    #messagebox
                    msgBox = QMessageBox()
                    msgBox.setText("More than 45 days late.  Need to evict!")
                    msgBox.exec()
                    #send inactive to db
                    unitID = PaymentDAO.getUnitID(whichUnitString)
                    evict = PaymentDAO.deActivate(unitID)
                    #confirmation on eviction
                    msgBox = QMessageBox()
                    msgBox.setText("Lessee deactivated from unit: " + whichUnitString)
                    msgBox.exec()
                    self.ui.textBrowser.setText("Lessee deactivated from unit: " + whichUnitString)
                elif (howLate > 30):
                    self.daysLate = 30
                    for row in late:
                        if row['daysLate'] == 30:
                            self.lateAmount = row['lateFee']
                    self.ui.textBrowser.setText("Monthly Amt $"+str(self.monthlyAmt)+"\nLate Fee $"+str(self.lateAmount)+"\nTotal $"+str(self.monthlyAmt+self.lateAmount))
                elif (howLate > 15):
                    self.daysLate = 15
                    for row in late:
                        if row['daysLate'] == 15:
                            self.lateAmount = row['lateFee']
                    self.ui.textBrowser.setText("Monthly Amt $"+str(self.monthlyAmt)+"\nLate Fee $"+str(self.lateAmount)+"\nTotal $"+str(self.monthlyAmt+self.lateAmount))
        else:
            self.ui.textBrowser.setText("Must select a unit")
                
    def recvPmt(self):
        #if unit selected then run showAmtOwed
        whichUnitString = self.ui.cmbLeasedUnits.currentText()
        if not(whichUnitString == "Select a unit") and (self.ui.textBrowser.toPlainText() == ""):
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

    def showPmtHistory(self):
        whichUnitString = self.ui.cmbLeasedUnits.currentText()
        PaymentDAO.getPayments(whichUnitString)
        print("show payments...")
        pass
                
                
                
            
        
        

       
    