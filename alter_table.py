import sqlite3
import pandas as pd

'''
con = sqlite3.connect("scheduler.db")
cur = con.cursor()
addColumn = "ALTER TABLE scheduleArchive ADD COLUMN finish VARCHAR(30)"
cur.execute(addColumn)

con.close()
'''

cnx = sqlite3.connect('scheduler.db')
df = pd.read_sql_query('SELECT * FROM scheduleArchive', cnx)

print(df)