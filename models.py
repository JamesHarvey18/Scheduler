from app import db
import hashlib, binascii, os
from db_setup import db_session
import pandas as pd
import pypyodbc

"""
This file is needed as a model of the database so the data can be entered
as well as queried in the proper format with SQLAlchemy. This class is used
in main.py. Do not make an object, simply use the class attributes like
"Drawing.job_number"
"""


class Schedule(db.Model):
    __tablename__ = "schedule"

    id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.Date)
    part_number = db.Column(db.String)
    part_description = db.Column(db.String)
    job_number = db.Column(db.Integer)
    work_number = db.Column(db.String)
    part_quantity = db.Column(db.Integer)
    part_location = db.Column(db.String)
    entry_time = db.Column(db.String)
    entry_date = db.Column(db.Date)
    employee_id = db.Column(db.String)
    comments = db.Column(db.String)
    revision = db.Column(db.String)
    material_status = db.Column(db.String)
    machine_center = db.Column(db.String)
    original_estimated_time = db.Column(db.String)
    quantity_complete = db.Column(db.String)
    actual_time = db.Column(db.String)
    archived = db.Column(db.Boolean)
    priority = db.Column(db.Integer)
    finish = db.Column(db.String)
    pdf = db.Column(db.String)
    location_deleted = db.Column(db.String)
    date_deleted = db.Column(db.Date)

    def get_pdf(self):
        cnxn = pypyodbc.connect("Driver={SQL Server};"
                                "Server=cvdpc93;"
                                "Database=CVD;"
                                "UID=READ_ONLY;pwd=Readonly20")

        sql = "SELECT URL_Document FROM CVD_PART_REV_ADD_DATE WHERE PartNumber = '" + self.part_number + "'"
        df = pd.read_sql_query(sql, cnxn)

        if not df.empty:
            url = df['url_document'].values[0]
        else:
            return ""
        url = "file:" + str(url)
        return url

    def get_revision(self):
        cnxn = pypyodbc.connect("Driver={SQL Server};"
                                "Server=cvdpc93;"
                                "Database=CVD;"
                                "UID=READ_ONLY;pwd=Readonly20")

        sql = "SELECT Revision FROM CVD_WO_WOOP_Rev2 WHERE [JOB NO] = '" + self.job_number + "' AND WORK_ORDER = '" \
              + self.work_number + "';"
        # operation = 0020???????????????????????????

        df = pd.read_sql_query(sql, cnxn)

        result = df['revision'].values[0]

        cnxn.close()

        return result

    def get_actual_time(self):
        cnxn = pypyodbc.connect("Driver={SQL Server};"
                                "Server=cvdpc93;"
                                "Database=CVD;"
                                "UID=READ_ONLY;pwd=Readonly20")

        sql = "SELECT SUM(HOURS_WORKED) FROM CVD_WO_WOOP_Rev2 WHERE [JOB NO] = '" + self.job_number\
              + "' AND WORK_ORDER = '" + self.work_number + "';"
        # operation = 0020???????????????????????????

        df = pd.read_sql_query(sql, cnxn)

        result = df.iloc[0, 0]

        cnxn.close()

        return result

    def get_part_number(self):
        cnxn = pypyodbc.connect("Driver={SQL Server};"
                                "Server=cvdpc93;"
                                "Database=CVD;"
                                "UID=READ_ONLY;pwd=Readonly20")

        sql = "SELECT CATALOGUE_NUMBER FROM CVD_WO_WOOP_Rev2 WHERE [JOB NO] = '" + self.job_number + "' AND WORK_ORDER = '" \
              + self.work_number + "';"
        # operation = 0020???????????????????????????

        df = pd.read_sql_query(sql, cnxn)

        result = df['catalogue_number'].values[0]

        cnxn.close()

        return result

    @staticmethod
    def get_job_number(barcode):
        job_number = barcode.split()[0]
        return job_number

    @staticmethod
    def get_work_order(barcode):
        work_order = barcode.split()[1]
        work_order = work_order[0:4]
        return work_order


    def get_machine_center(self):
        cnxn = pypyodbc.connect("Driver={SQL Server};"
                                "Server=cvdpc93;"
                                "Database=CVD;"
                                "UID=READ_ONLY;pwd=Readonly20")

        sql = "SELECT WORK_CENTER FROM CVD_WO_WOOP_Rev2 WHERE [JOB NO] = '" + self.job_number + "' AND WORK_ORDER = '" \
              + self.work_number + "' AND OPERATION = '0020';"
        # operation = 0020???????????????????????????

        df = pd.read_sql_query(sql, cnxn)

        result = df['work_center'].values[0]

        cnxn.close()

        return result

    def get_description(self):
        cnxn = pypyodbc.connect("Driver={SQL Server};"
                                "Server=cvdpc93;"
                                "Database=CVD;"
                                "UID=READ_ONLY;pwd=Readonly20")

        sql = "SELECT Description FROM PartMaster WHERE PartNumber = '" + self.part_number + "';"

        df = pd.read_sql_query(sql, cnxn)

        cnxn.close()

        result = df['description'].values

        if len(result) != 0:
            return result[0]
        else:
            result = "None"
            return result

    def get_quantity(self):
        cnxn = pypyodbc.connect("Driver={SQL Server};"
                                "Server=cvdpc93;"
                                "Database=CVD;"
                                "UID=READ_ONLY;pwd=Readonly20")

        sql = "select QTY_REQUIRED from CVD_WO_WOOP_Rev2 where CATALOGUE_NUMBER = '"\
              + str(self.part_number) + "' and [JOB NO] = '" + self.job_number\
              + "' and WORK_ORDER = '" + self.work_number + "';"

        df = pd.read_sql_query(sql, cnxn)
        cnxn.close()
        result = int(df['qty_required'].values[0])

        return result


class User(db.Model):
    __tablename__ = "user_account"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

    @staticmethod
    def hash_password(password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def verify(self):
        stored_password = self.get_stored_password()
        if stored_password is None:
            return False
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

    def get_stored_password(self):
        qry = db_session.query(User).filter(User.username == self.username)
        qry = qry.first()

        if qry is None:
            return None

        stored_password = qry.password
        db_session.commit()
        return stored_password

    def add_password(self, name, password_string):
        password = Password()
        password.username = name
        password.password = self.hash_password(password_string)

        qry = db_session()
        qry.add(password)
        qry.commit()


class Password(db.Model):
    __tablename__ = "passwords"

    id = db.Column(db.Integer, primary_key=True)
    password_name = db.Column(db.String)
    encrypted_password = db.Column(db.String)

