import mysql.connector
from mysql.connector import errorcode
from mysql.connector.errors import *

configRegular = {
            'user': 'stouser',
            'password': 'JuWpeNQxjv87k32@bcE',
            'host': 'localhost',
            'database': 'storagetoo',
            'raise_on_warnings': True
            }
try:
    conn = mysql.connector.connect(**configRegular)
    conn.autocommit = False
    cursor = conn.cursor(buffered=True,dictionary=True)
    query = "SELECT * FROM users"
    cursor.execute(query)
    allUsers = cursor.fetchall()
    
    
    cursor.close()
    cursor = conn.cursor(buffered=True,dictionary=True)
    query = "SELECT * FROM sizes"
    cursor.execute(query)
    allSizes = cursor.fetchall()
    cursor.close()
except mysql.connector.Error as e:
            print("Error while connecting to MySQL", e)
'''run a query
close the cursor
test the cursor, reopen if necessary
run another query'''