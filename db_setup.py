from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

"""
File for setting up the database and allowing connections to it in main.py
Anytime you want to access the db in main.py, you must make a db_session() object.
Init_db() must be called at start of main.py file.
You must commit (db_session.commit()) and session objects you create in main.py to
prevent any SQLite errors.
"""

engine = create_engine('sqlite:///scheduler.db', connect_args={'check_same_thread': False}, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)
