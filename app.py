from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# This file configures the flask app
# Assigns the sqlite database that is created to the flask app
# Creates an object of the SQLAlchemy class named db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scheduler.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = '191kajdf 0a9dfdfeee'
db = SQLAlchemy(app)
