from sqlalchemy import Column, Integer, String, Date, create_engine, Boolean, update
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///scheduler.db', echo=True)
base = declarative_base()


class Schedule(base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True)
    due_date = Column(String)
    part_number = Column(String)
    part_description = Column(String)
    job_number = Column(Integer)
    work_number = Column(String)
    part_quantity = Column(Integer)
    part_location = Column(String)
    entry_time = Column(String)
    entry_date = Column(Date)
    employee_id = Column(String)
    comments = Column(String)
    revision = Column(String)
    material_status = Column(String)
    machine_center = Column(String)
    original_estimated_time = Column(String)
    revised_estimated_time = Column(String)
    actual_time = Column(String)
    quantity_complete = Column(String)
    mtl = Column(String)
    archived = Column(Boolean)
    priority = Column(Integer)
    finish = Column(String)

    def __repr__(self):
        return "{}".format(self.name)


class ScheduleArchive(base):
    __tablename__ = "scheduleArchive"

    id = Column(Integer, primary_key=True)
    due_date = Column(String)
    part_number = Column(String)
    part_description = Column(String)
    job_number = Column(Integer)
    work_number = Column(String)
    part_quantity = Column(Integer)
    part_location = Column(String)
    entry_time = Column(String)
    entry_date = Column(Date)
    employee_id = Column(String)
    comments = Column(String)
    revision = Column(String)
    material_status = Column(String)
    machine_center = Column(String)
    original_estimated_time = Column(String)
    revised_estimated_time = Column(String)
    actual_time = Column(String)
    quantity_complete = Column(String)
    mtl = Column(String)
    archived = Column(Boolean)
    priority = Column(Integer)
    finish = Column(String)

    def __repr__(self):
        return "{}".format(self.name)


class User(base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)


class Password(base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True)
    password_name = Column(String)
    encrypted_password = Column(String)

    def __repr__(self):
        return "{}".format(self.name)


base.metadata.create_all(engine)
