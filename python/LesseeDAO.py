import mysql.connector
from mysql.connector import Error
from dbUtil import Database

class LesseeDAO:
    def getMonthlyAmt(whichUnit):
        db = Database()
        amt = db.getMonthlyPrice(whichUnit)
        return amt
    
    def insertPayment(self, whichUnit, amt, today, dueDate):
        db = Database()
        db.dbCommitPayment(whichUnit, amt, today, dueDate)

    def insertLessee(self, *args):
        db = Database()
        db.dbCommitPayment(*args[0:4])
        db.insertLessee(*args[4:11], *args[0:1])