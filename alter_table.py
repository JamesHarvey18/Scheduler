import sqlite3
import pandas as pd


con = sqlite3.connect("scheduler.db")
cur = con.cursor()
addColumn = "DELETE FROM user_account"
cur.execute(addColumn)
con.commit()

con.close()