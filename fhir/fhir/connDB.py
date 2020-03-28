import mysql.connector
db = mysql.connector.connect(host='localhost',user='root',passwd='123456.abc')
cursor = db.cursor()
query = ("SHOW DATABASES")
cursor.execute(query)
for r in cursor:
    print(r)
