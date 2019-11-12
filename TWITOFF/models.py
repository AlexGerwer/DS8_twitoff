"""The database models"""

from flask_sqlalchemy import SQLAlchemy

# Import database capital letter for global scope
DB = SQLAlchemy()

class User(DB.Model):
    """Twitter users for analysis"""
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)

class Tweet(DB.Model):
    """Twitter users' tweets for analysis"""
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Unicode(280))
