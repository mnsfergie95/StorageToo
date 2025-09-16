from dbUtil import Database
from Lessee import Lessee

class LesseeDAO:
    def getMonthlyAmt(whichUnit):
        db = Database('regular')
        amt = db.getMonthlyPrice(whichUnit)
        return amt
    
    def insertPayment(self, whichUnit, amt, today, dueDate):
        db = Database('regular')
        db.dbCommitPayment(whichUnit, amt, today, dueDate)

    def insertLessee(*args):
        db = Database('regular')
        db.dbCommitPayment(*args[0:4])
        db.insertLessee(*args[4:11], *args[0:1])

    def getLesseeFromResultSet(self, lessee):
        lessor = Lessee(*lessee)
        
    def searchLessee(name, unit, phone):
        db = Database('regular')
        lessee = db.searchLessee(name,unit,phone)
        return lessee

    def populateCurrentLessees():
        db = Database('regular')
        lessees = db.getAllCurrentLessees()
        return lessees
    
    def populateFormerLessees():
        db = Database('regular')
        lessees = db.getAllFormerLessees()
        return lessees
        