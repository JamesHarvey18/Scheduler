import sqlite3

con = sqlite3.connect("scheduler.db")
cur = con.cursor()
addColumn = "ALTER TABLE schedule ADD COLUMN finish VARCHAR(30)"
cur.execute(addColumn)

con.close()