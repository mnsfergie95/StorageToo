from PyQt6.QtWidgets import QMessageBox, QDialog
from UI.dlgPayment_ui import Ui_dlgPayment
from dbUtil import Database
from PaymentDAO import PaymentDAO
from datetime import date

class Payment(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_dlgPayment()
        self.ui.setupUi(self)

    def populateCmbLeasedUnits(self):
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
        if (whichUnitString is not None):
            pmt = PaymentDAO.getLastPayment(whichUnitString)
            if (pmt != None):
                monthlyPrice = PaymentDAO.getMonthlyAmt(whichUnitString)
                monthlyAmt = monthlyPrice['monthly_price']
                nextDueDate = pmt[0]['NextDueDate']
                #print('type is ', type(nextDueDate))
                #dueDate = date(nextDueDate)
                newDueDate = self.add_month(nextDueDate)
                print('dueDate is ', nextDueDate)
                print('newDueDate is ', newDueDate)
                print('monthly amt is ', monthlyAmt)
                
                
                
            
        
        

       
    