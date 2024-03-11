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
            self.conn.autocommit = False
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

    def searchLessee(self, name, label, phone):
        try:
            args = (name, label, phone)
            print("name is ",name," label is ",label," phone is ",phone)
            self.cursor.callproc('procSearch', args)
            self.cursor.stored_results
            for result in self.cursor.stored_results():
                lessee = result.fetchall()
                self.cursor.close()
                return lessee
        except mysql.connector.Error as e:
            print("Error while searching lessee", e)

    def insertLessee(self, name, addrL1, addrL2, city, state, zipCode, phone, label):
        try:
            args = (name, addrL1, addrL2, city, state, zipCode, phone, label)
            self.cursor.callproc('procAddLessee', args)
            self.conn.commit()
        except mysql.connector.Error as e:
            print("Error while inserting new lessee", e)

    def dbCommitPayment(self, whichUnit, amt, today, firstOfNextMonth):
        try:
            args = (whichUnit, amt, today, firstOfNextMonth,)
            self.cursor.callproc('procCommitPmt', args)
            self.conn.commit()
            #print("rows affected is ", self.cursor.rowcount)
        except mysql.connector.Error as e:
            print("Error while committing payment", e)

    def getAllLessees(self):
        try:
            lessees = []
            self.cursor.callproc('procGetAllLessees')
            self.cursor.stored_results
            for result in self.cursor.stored_results():
                lessee = result.fetchall()
                lessees.append(lessee)
            self.cursor.close()
            return lessees
        except mysql.connector.Error as e:
            print("Error while getting all lessees", e)
        
    def getLastPayment(self, whichUnit):
        try:
            args = (whichUnit, )
            self.cursor.callproc('procGenerateLastPayment', args)
            self.cursor.stored_results
            for result in self.cursor.stored_results():
                pmt = result.fetchall()
            self.cursor.close()
            return pmt
        except mysql.connector.Error as e:
            print("Error while getting last payment", e)
        
    def getUnitID(self, label):
        try:
            args = (label, )
            self.cursor.callproc('procFindUid', args)
            self.cursor.stored_results
            for result in self.cursor.stored_results():
                unit_id = result.fetchone()
            self.cursor.close()
            return unit_id['unitid']
        except mysql.connector.Error as e:
            print("Error while getting last payment", e)

    def deActivate(self, unit_id):
        try:
            args = (unit_id, )
            self.cursor.callproc('procDeactivateLessee', args)
            self.conn.commit()
            self.cursor.close()
        except mysql.connector.Error as e:
            print("Error while getting last payment", e)

    def getLateFees(self):
        try:
            #args = (unit_id, )
            self.cursor.callproc('procGetLateFees')
            self.cursor.stored_results
            for result in self.cursor.stored_results():
                lateFees = result.fetchall()
            self.cursor.close()
            return lateFees
        except mysql.connector.Error as e:
            print("Error while getting last payment", e)       

    def getPayments(self, unit):
        try:
            args = (unit, )
            self.cursor.callproc('procGetAllPaymentsOnUnit', args)
            self.cursor.stored_results
            for result in self.cursor.stored_results():
                Payments = result.fetchall()
            self.cursor.close()
            return Payments
        except mysql.connector.Error as e:
            print("Error while getting last payment", e)     
        pass