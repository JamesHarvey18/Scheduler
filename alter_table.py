import sqlite3

con = sqlite3.connect("scheduler.db")
cur = con.cursor()
addColumn = "ALTER TABLE schedule ADD COLUMN due_date varchar(32)"
cur.execute(addColumn)

con.close()