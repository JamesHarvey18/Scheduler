import sqlite3
import pandas as pd


con = sqlite3.connect("scheduler.db")
cur = con.cursor()
addColumn = "ALTER TABLE schedule ADD location_deleted varchar(255)"
cur.execute(addColumn)
con.commit()

con.close()
