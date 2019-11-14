from decouple import config
from dotenv import load_dotenv
from flask import Flask, render_template, request#
from .models import DB, User
from .twitter import add_or_update_user
from .predict import predict_user

load_dotenv

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

    # Add a route to add or get users or haanle error
    @app.route('/user', methods=['POST']) # uses a form
    @app.route('/user/<name>', methods=['GET']) # uses a parameter
    def user(name=None, message=''):
        # Add this line in last
        name = name or request.values['user_name']
        # import pdb; pdb.set_trace()
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e: # handles an error
            message = "Error adding {}: {}".format(name,e)
            tweets=[]
        return render_template('user.html', title=name, tweets=tweets,
        message=message)

    # Add a route for the predictions
    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        # Rule out requests that do not involve different users
        if user1 == user2:
            message = 'Requires different users for comparison'
        else:
            prediction = predict_user(user1, user2, request.values['tweet_text'])
            message = '"{}" is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], user1 if prediction else user2,
                user2 if prediction else user1)
        return render_template('prediction.html', title='Prediction', message=message)

    # Add reset route for convenience
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset', users=[])

    return app
