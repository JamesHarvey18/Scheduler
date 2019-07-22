import sqlite3
import pandas as pd


con = sqlite3.connect("scheduler.db")
cur = con.cursor()
addColumn = "UPDATE schedule SET job_number='ST0237' WHERE job_number='st0237'"
cur.execute(addColumn)
con.commit()

con.close()