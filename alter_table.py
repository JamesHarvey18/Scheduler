import sqlite3

con = sqlite3.connect("scheduler.db")
cur = con.cursor()
addColumn = "ALTER TABLE schedule ADD COLUMN priority INTEGER"
cur.execute(addColumn)

con.close()