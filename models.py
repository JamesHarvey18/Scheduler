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
    revised_estimated_time = db.Column(db.String)
    quantity_complete = db.Column(db.String)
    actual_time = db.Column(db.String)

    def get_machine_center(self):
        cnxn = pypyodbc.connect("Driver={SQL Server};"
                                "Server=cvdpc93;"
                                "Database=CVD;"
                                "UID=READ_ONLY;pwd=Readonly2019")

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
                                "UID=READ_ONLY;pwd=Readonly2019")

        df = pd.read_sql_query('select PartNumber, Description '
                               'from PartMaster ', cnxn)
        cnxn.close()

        result = df.loc[df['partnumber'] == self.part_number]['description'].values

        if len(result) != 0:
            return result[0]
        else:
            result = "None"
            return result

    @staticmethod
    def get_quantity(part_number, release_wo):
        cnxn = pypyodbc.connect("Driver={SQL Server};"
                                "Server=cvdpc93;"
                                "Database=CVD;"
                                "UID=READ_ONLY;pwd=Readonly2019")

        sql = "select QTY_REQUIRED from CVD_WO_WOOP_Rev2 where CATALOGUE_NUMBER = '"\
              + str(part_number) + "' and [JOB NO] = '" + release_wo.split()[0]\
              + "' and WORK_ORDER = '" + release_wo.split()[1] + "';"

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

