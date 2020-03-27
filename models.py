"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False,
                           unique=False)
    last_name = db.Column(db.String(50),
                          nullable=False,
                          unique=False)
    profile_img = db.Column(db.String,
                            nullable=True,
                            default='https://cdn.pixabay.com/photo/2014/08/27/12/58/penguins-429128_960_720.jpg')


class Post(db.Model):
    """Post"""
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False,
                      unique=False)
    content = db.Column(db.String(1000),
                        nullable=False,
                        unique=False)
    created_at = db.Column(db.DateTime,
                           default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    users = db.relationship('User', backref='posts')


class Tag(db.Model):
    """Tag"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(20),
                     nullable=False,
                     unique=True)

    posts = db.relationship('Post',
                            secondary='posttags',
                            backref='tags')


class PostTag(db.Model):
    """Post Tag Combo"""

    __tablename__ = "posttags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'),
                        primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'),
                       primary_key=True)

    tags = db.relationship('Tag', backref='posttags')
    posts = db.relationship('Post', backref='posttags')
