import sqlite3
import os

print("Current folder:", os.getcwd())

conn = sqlite3.connect("healthcare.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM predictions")

rows = cursor.fetchall()

print("Total Records:", len(rows))

for row in rows:
    print(row)

conn.close()