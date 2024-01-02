from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.errors import *
import sys

class Database:
    config = {
            'host':'localhost',
            'database':'storagetoo',
            'user':'root',
            'password': 'sharon1354'
            }
    
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
        except mysql.connector.Error as e:
            print("Error while connecting to MySQL", e)

    def __del__(self):
        #if isinstance(self.conn, mysql.connector.connection):
        self.conn.close()

    def populateList_AvailUnits(self):
        try:
            self.cursor.callproc('procListAllAvailUnits')
            self.cursor.stored_results
            # populate unit_list with results
            for result in self.cursor.stored_results():
                unit_list = result.fetchall()
            self.cursor.close()
            return unit_list
        except mysql.connector.Error as e:
            print("Error while populating avail unit list", e)

    def populateList_LeasedUnits(self):
        try:
            self.cursor.callproc('procListAllLeasedUnits')
            self.cursor.stored_results
            # populate unit_list with results
            for result in self.cursor.stored_results():
                unit_list = result.fetchall()
            self.cursor.close()
            return unit_list
        except mysql.connector.Error as e:
            print("Error while populating leased unit list", e)

    def getMonthlyPrice(self, whichUnit)->float:
        try:
            args = (whichUnit,)
            self.cursor.callproc('procMonthly', args)
            self.cursor.stored_results
            for result in self.cursor.stored_results():
                amt = result.fetchall()
            self.cursor.close()
            return amt[0]
        except mysql.connector.Error as e:
            print("Error while getting monthly unit price", e)

    def insertLessee(self, name, addrL1, addrL2, city, state, zipCode, phone, label):
        try:
            args = (name, addrL1, addrL2, city, state, zipCode, phone, label)
            self.cursor.callproc('procAddLessee', args)
        except mysql.connector.Error as e:
            print("Error while inserting new lessee", e)

    def dbCommitPayment(self, whichUnit, amt, firstOfThisMonth):
        try:
            args = (whichUnit, amt, firstOfThisMonth)
            self.cursor.callproc('procCommitPmt', args)
        except mysql.connector.Error as e:
            print("Error while inserting new lessee", e)
