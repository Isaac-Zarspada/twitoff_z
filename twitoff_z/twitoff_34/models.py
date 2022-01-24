from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    # id column schema
    id = DB.column(DB.BigInteger, primary_key=True, nullable=False)
    # username column schema
    username = DB.column(DB.String, nullable=False)


class Tweet(DB.Model):
    # ID column schema
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # text schema
    test = DB.Column(DB.Unicode(300), nullable=False)
    # user column schema
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'),
                        nullable=False)
    user = DB.relationship("User", backref=DB.backref('tweets'),lazy=True)
