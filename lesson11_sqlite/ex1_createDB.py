import sqlite3
conn = sqlite3.connect('../lesson11_sql-light/test.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        name TEXT NOT NULL, 
                        email TEXT NOT NULL UNIQUE, 
                        age INTEGER);''')
# cursor.commit()
# cursor.execute('''INSERT INTO users (name, email, age) VALUES ("Ivan", "ssdwqafdx@ddcsrd", "25");''', ())
# conn.commit()

cursor.execute('SELECT * FROM users')
cursor.execute('SELECT * FROM users WHERE name = "Ivan"')
# cursor.close()
# conn.close()
# афiнованiсть типiв
print(cursor.fetchall()) # взять все