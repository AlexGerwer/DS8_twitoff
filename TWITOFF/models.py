"""The database models"""

from flask_sqlalchemy import SQLAlchemy

# Import database capital letter for global scope
DB = SQLAlchemy()

class User(DB.Model):
    """Twitter users for analysis"""
    # id = DB.Column(DB.Integer, primary_key=True)
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)
    # newest_tweet_id = DB.Column(DB.Integer)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Tweet(DB.Model):
    """Twitter users' tweets for analysis"""
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Unicode(280))
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets'), lazy=True)

    # Added for pickling data
    embedding = DB.Column(DB.PickleType, nullable=False)

    def __repr__(self):
        return '<Tweet {}>'.format(self.text)
