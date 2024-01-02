import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import QFile
from UI.MainWindow_ui import Ui_MainWindow
from dbUtil import Database
#from filename import classname
import re
from datetime import datetime, time, date, tzinfo, timedelta
import calendar
from LesseeDAO import LesseeDAO

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def populateCmbAvailUnits(self):
        db = Database()
        list = db.populateList_AvailUnits()
        for name in list:
            window.ui.cmbUnitsAvail.addItem(name['label'])
                
    def populateCmbLeasedUnits(self):
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
    
    ''' Add a lessee to DB '''
    def insertLessee(self):
        # check for minimum data entry requirement...name,unit, and phone
        label = window.ui.cmbUnitsAvail.currentText()
        name = window.ui.txtName.text()
        phone = window.ui.txtPhone.text()
        window.ui.textBrowserResult.setText("")
        if ((label is not None) and (name is not None) and (phone is not None)):
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
            input_dt = datetime.now()
            res = calendar.monthrange(input_dt.year, input_dt.month)
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
            #insert partial payment into db
            #clear the form values
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.ui.btnAddLessee.clicked.connect(window.insertLessee)
    window.populateCmbAvailUnits()
    window.populateCmbLeasedUnits()
    window.show()

    sys.exit(app.exec())

    