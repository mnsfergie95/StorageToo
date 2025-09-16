from dbUtil import Database

class PaymentDAO():
    def getLastPayment(unit):
        db = Database('regular')
        pmt = db.getLastPayment(unit)
        return pmt
    
    def getMonthlyAmt(unit):
        db = Database('regular')
        monthlyAmt = db.getMonthlyPrice(unit)
        return monthlyAmt
        
    def getUnitID(label):
        db = Database('regular')
        unitID = db.getUnitID(label)
        return unitID
    
    def deActivate(unit_id):
        db = Database('regular')
        db.deActivate(unit_id)
        return True
    
    def getLateFees():
        db = Database('regular')
        return db.getLateFees()
    
    def commitPmt(unit, amtOwed, todayDate, nextDueDate):
        db = Database('regular')
        db.dbCommitPayment(unit, amtOwed, todayDate, nextDueDate)

    def getPayments(unit):
        db = Database('regular')
        db.getPayments(unit)