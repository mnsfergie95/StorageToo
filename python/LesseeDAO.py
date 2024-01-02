import mysql.connector
from mysql.connector import Error
from dbUtil import Database

class LesseeDAO:
    def getMonthlyAmt(whichUnit):
        db = Database()
        amt = db.getMonthlyPrice(whichUnit)
        return amt
    
    def insertPartialPayment(whichUnit, amt):
        db = Database()
        db.placeInitialPayment(whichUnit, amt)