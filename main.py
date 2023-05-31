import sqlite3

conn = sqlite3.connect('./db/worldcup.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM tournaments')

results = cursor.fetchall()

for row in results:
    print(row)
    
conn.close()