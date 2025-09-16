from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.errors import *
import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from PyQt6.QtWidgets import QMessageBox

class Database():
    configRegular = {
            'user': 'stouser',
            'password': 'JuWpeNQxjv87k32@bcE',
            'host': 'localhost',
            'database': 'storagetoo',
            'raise_on_warnings': True
            }
    configAdmin = {
            'user': 'stoadmin',
            'password': 'Zjq&NcB38L1hApgI2kj',
            'host': 'localhost',
            'database': 'storagetoo',
            'raise_on_warnings': True
    }

#userType is either 'regular' or 'admin'

    def __init__(self, userType):
        try:
            if (userType == "regular"):
                self.conn = mysql.connector.connect(**self.configRegular)
                self.conn.autocommit = False
                
            if (userType == "admin"):
                self.conn = mysql.connector.connect(**self.configAdmin)
                self.conn.autocommit = False
                
            #self.cursor.close()
        except mysql.connector.Error as e:
            print("Error while connecting to MySQL", e)

    def __del__(self):
        #if isinstance(self.conn, mysql.connector.connection):
        if 'self.cursor' in locals() and self.cursor:
            self.cursor.close()
        self.conn.close()

    def fetchAllUsers(self):
        try:
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
            query = "SELECT username FROM users"
            self.cursor.execute(query)
            allUsers = self.cursor.fetchall()
            self.cursor.close()
            return allUsers 
        except mysql.connector.Error as e:
            print("error writing fetching all users from db", e)

    def writeNewUserToDB(self,username):
        try:
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
            query = "SELECT * FROM users WHERE username = %s"
            self.cursor.execute(query,(username,))
            self.cursor.fetchall()
            if not(self.cursor.rowcount == 0):
                self.cursor.close()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText("Username already exists.")
                msg.setWindowTitle("Failure")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                msg.exec()
                return False
            else:
                query = "INSERT INTO users (username) VALUES (%s)"
                if (self.conn.in_transaction):
                    self.conn.commit()
                self.conn.start_transaction()
                self.cursor.execute(query, (username,))
                self.conn.commit()
                self.cursor.close()
                return True
        except mysql.connector.Error as e:
            print("error writing new user password to db", e)

    def writeNewUserPasswordToDB(self, username, password):
        key = get_random_bytes(16)
        data = password.encode('utf-8')
        cipher = AES.new(key, AES.MODE_GCM)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)
        try:
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
            self.conn.start_transaction()
            query = ("UPDATE users set tag=%s WHERE username = %s")
            self.cursor.execute(query, (tag,username))
            query = ("UPDATE users set nonce=%s WHERE username = %s")
            self.cursor.execute(query, (nonce,username))
            query = ("UPDATE users set theKey=%s WHERE username = %s")
            self.cursor.execute(query, (key,username))
            query = ("UPDATE users set ciphertext=%s WHERE username = %s")
            self.cursor.execute(query, (ciphertext, username,))
            self.conn.commit()
            self.cursor.close()
        except mysql.connector.Error as e:
            print("error writing admin password to db", e)

    def readUserPassword(self, username):
        try:
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
            query = ("SELECT * FROM users WHERE username = %s")
            self.cursor.execute(query, (username,))
            data = self.cursor.fetchall()
            self.conn.commit()
            self.cursor.close()
        except mysql.connector.Error as e: 
            print("error reading admin password from db", e)
        if data:
            for row in data:
                tag = row['tag']
                nonce = row['nonce']
                key = row['theKey']
                ciphertext = row['ciphertext']
        #password = tag + nonce + key + ciphertext
        #           16     16      16     28
        decipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        try:
            decrypted_plaintext = decipher.decrypt_and_verify(ciphertext, tag)
            return decrypted_plaintext
        except ValueError as e:
            print("Decryption failed or data tampered: ", e)

    def isUserInDB(self, username):
        try:
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
            query = ("SELECT * FROM users WHERE username = %s")
            self.cursor.execute(query, (username,))
            if not(self.cursor.rowcount == 0):
                self.cursor.close()
                return True
            else:
                self.cursor.close()
                return False
        except mysql.connector.Error as e:
            return False
        
    def populateList_AvailUnits(self):
        try:
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
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
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
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
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
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
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
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
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
            self.cursor.callproc('procAddLessee', args)
            self.conn.commit()
            self.cursor.close()
        except mysql.connector.Error as e:
            print("Error while inserting new lessee", e)

    def dbCommitPayment(self, whichUnit, amt, today, firstOfNextMonth):
        try:
            args = (whichUnit, amt, today, firstOfNextMonth,)
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
            self.cursor.callproc('procCommitPmt', args)
            self.conn.commit()
            #print("rows affected is ", self.cursor.rowcount)
            self.cursor.close()
        except mysql.connector.Error as e:
            print("Error while committing payment", e)

    def getAllCurrentLessees(self):
        try:
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
            lessees = []
            self.cursor.callproc('procGetAllCurrentLessees')
            self.cursor.stored_results
            for result in self.cursor.stored_results():
                lessee = result.fetchall()
                lessees.append(lessee)
            self.cursor.close()
            return lessees
        except mysql.connector.Error as e:
            print("Error while getting all lessees", e)
    
    def getAllFormerLessees(self):
        try:
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
            lessees = []
            self.cursor.callproc('procGetAllFormerLessees')
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
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
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
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
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
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
            self.cursor.callproc('procDeactivateLessee', args)
            self.conn.commit()
            self.cursor.close()
        except mysql.connector.Error as e:
            print("Error while getting last payment", e)

    def getLateFees(self):
        try:
            #args = (unit_id, )
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
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
            self.cursor = self.conn.cursor(buffered=True,dictionary=True)
            self.cursor.callproc('procGetAllPaymentsOnUnit', args)
            self.cursor.stored_results
            for result in self.cursor.stored_results():
                Payments = result.fetchall()
            self.cursor.close()
            return Payments
        except mysql.connector.Error as e:
            print("Error while getting last payment", e)     
        pass