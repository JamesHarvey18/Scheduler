import sqlite3
import pandas as pd


con = sqlite3.connect("scheduler.db")
cur = con.cursor()
addColumn = "UPDATE schedule SET priority = 99 WHERE priority IS NULL"
cur.execute(addColumn)
con.commit()

con.close()
