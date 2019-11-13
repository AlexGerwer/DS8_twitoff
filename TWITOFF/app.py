from decouple import config
from flask import Flask, render_template, request#
from .models import DB, User

# Create an app factory

def create_app():
    app = Flask(__name__)

    # Add configuration
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    # Change so that changes can be made in the .env file
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    # Eliminate warning message on running the file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Link the app and the database
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        # return 'Welcome to Twitoff'
        # return render_template('base.html')
        # return render_template('base.html', title='Home')
        return render_template('base.html', title='Home', users=users)

    # Add reset route for convenience
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset', users=[])

    return app
