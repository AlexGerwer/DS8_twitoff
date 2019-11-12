from flask import Flask
from .models import DB

# Create an app factory

def create_app():
    app = Flask(__name__)

    # Add configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    # Link the app and the database
    DB.init_app(app)

    @app.route('/')
    def root():
        return 'Welcome to Twitoff'
    return app
