from dbUtil import Database

class PaymentDAO():
    def getLastPayment(unit):
        db = Database()
        pmt = db.getLastPayment(unit)
        return pmt
    
    def getMonthlyAmt(unit):
        db = Database()
        monthlyAmt = db.getMonthlyPrice(unit)
        return monthlyAmt
        
    def getUnitID(label):
        db = Database()
        unitID = db.getUnitID(label)
        return unitID
    
    def deActivate(unit_id):
        db = Database()
        db.deActivate(unit_id)
        return True
    
    def getLateFees():
        db = Database()
        return db.getLateFees()
    
    def commitPmt(unit, amtOwed, todayDate, nextDueDate):
        db = Database()
        db.dbCommitPayment(unit, amtOwed, todayDate, nextDueDate)