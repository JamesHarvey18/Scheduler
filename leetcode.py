import pandas as pd
import xlrd
import main
from models import Schedule
import datetime
from main import preprocess_date
from db_setup import db_session


df = pd.read_excel('jobscope.xlsx')


for i in range(df.size):
    try:
        schedule = Schedule()
        dt = datetime.datetime.now()
        barcode = df.iloc[i].values[0]

        schedule.due_date = datetime.date(2019, 8, 6)
        schedule.job_number = schedule.get_job_number(barcode).upper()  # Manual
        schedule.work_number = schedule.get_work_order(barcode)  # Manual
        schedule.part_number = schedule.get_part_number()
        schedule.part_description = schedule.get_description()  # Jobscope

        try:
            schedule.part_quantity = schedule.get_quantity()  # Jobscope
        except Exception as e:
            print(str(e))
            schedule.part_quantity = 0

        schedule.part_location = 'Machine Shop' # Auto
        schedule.entry_time = dt.strftime("%H:%M:%S")  # Auto
        schedule.entry_date = datetime.date.today()  # Auto
        schedule.machine_center = schedule.get_machine_center()  # schedule.get_machine_center()  # Manual
        schedule.actual_time = schedule.get_actual_time()  # Jobscope
        schedule.archived = 0
        schedule.pdf = schedule.get_pdf()

        qry = db_session()
        qry.add(schedule)
        qry.commit()
    except:
        print('failed ' + df.iloc[i].values[0])
