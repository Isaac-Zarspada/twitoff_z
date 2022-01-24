from flask import Flask, render_template
from psutil import users
from .models import DB, User, Tweet

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

    @app.route("/")
    def hello_world():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)
    
    @app.route('/populate')
    def populate():
        # auto reset
        DB.drop_all()
        DB.create_all()

        # new users
        lis = User(id=1, username='lisellezee')
        javi = User(id=2, username='javizee')

        # new tweets
        twt1 = Tweet(id=1, test="liselle's tweet", user = lis)
        twt2 = Tweet(id=2, text='''the lowest form of intelligence is basing a conversation on 
                                a person and their attributes''', user = javi)

        # adding the users/tweets to the db session
        DB.session.add(lis)
        DB.session.add(javi)
        DB.session.add(twt1)
        DB.session.add(twt2)
        # making those changes permanent
        DB.session.commit()

    
    @app.route('/reset')
    def reset():
        # empty db
        DB.drop_all()
        # recreate tables
        DB.create_all()
        return 'This is a reset page'

    return app