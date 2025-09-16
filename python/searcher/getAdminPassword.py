from dbUtil import Database

#get admin password

db = Database('regular')
print(db.readUserPassword("demo"))
