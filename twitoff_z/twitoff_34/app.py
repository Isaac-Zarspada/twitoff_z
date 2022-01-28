from flask import Flask, render_template, request
from .models import DB, User, Tweet
from os import getenv
from .twitter import add_or_update_user
from .predict import predict_user

def create_app():
    app = Flask(__name__)

    # configuration to app
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # connect database to app
    DB.init_app(app)

    @app.route("/")
    def homepage():
        # query for users in database 
        return render_template('base.html', title='Home', users=User.query.all())

    @app.route('/reset')
    def reset():
        # empty db
        DB.drop_all()
        # recreate tables
        DB.create_all()

        return render_template('base.html', title='database has been reset')

    @app.route('/update')
    def update():

        usernames = get_usernames()
        for username in usernames:
            add_or_update_user(username)

        DB.session.commit()
        return render_template('base.html', title='Users have been updated')

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(username=None, message=''):
        username = username or request.values['user_name']
        try:
            if request.methods=='POST':
                add_or_update_user(username)
                message = f'User {username} added!'
        except Exception as e:
            message = f'Error adding {username}: {e}'
            tweets = []

        return render_template('user.html', title=username, tweets=tweets, message=message)
    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted([request.values['user0'], request.values['user1']])
        if user0 == user1:
            message = 'User entered twice!'
        else:
            prediction = predict_user
            message = "'{}' is more likely to be said by {} than {}".format(request.values['tweet_text'],
                                                                                            user1 if prediction else user0,
                                                                                            user0 if prediction else user1)
        return render_template('prediction.html', title='Prediction', message=message)
    return app


def get_usernames():
    Users = User.query.all()
    usernames = []
    for user in Users:
        usernames.append(user.username)
    return usernames