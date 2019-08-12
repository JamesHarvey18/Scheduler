import sqlite3
import pandas as pd


con = sqlite3.connect("scheduler.db")
cur = con.cursor()
addColumn = "DELETE FROM user_account"
sql = 'SELECT * FROM schedule WHERE job_number = "N-1275"'
update = 'UPDATE schedule SET machine_center = "NONE" WHERE machine_center = "None"'
cur.execute(addColumn)
con.commit()

con.close()
