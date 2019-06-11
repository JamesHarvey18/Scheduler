from app import db
import hashlib, binascii, os
from db_setup import db_session

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
    mtl = db.Column(db.String)


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

    @staticmethod
    def verify_password(stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

    def get_stored_password(self, name):
        qry = db_session.query(User).filter(User.username == name)
        qry = qry.first()
        stored_password = qry.password
        db_session.commit()
        return stored_password

    def add_password(self, name, password_string):
        password = Password()
        password.password_name = name
        password.encrypted_password = self.hash_password(password_string)

        qry = db_session()
        qry.add(password)
        qry.commit()


class Password(db.Model):
    __tablename__ = "passwords"

    id = db.Column(db.Integer, primary_key=True)
    password_name = db.Column(db.String)
    encrypted_password = db.Column(db.String)

