# -*- coding: utf-8 -*-
from app import db
from datetime import datetime


class User(db.Model):
    #id = db.Column('user_id', db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    pw_hash = db.Column(db.String(100))
    messages = db.relationship("Message", backref='user', lazy='dynamic')
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))

    def __init__(self, username, pw_hash):
        self.username = username.strip()
        self.pw_hash = pw_hash.strip()

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, index=True)
    messages = db.relationship("Message", backref='channel', lazy='dynamic')
    users = db.relationship("User", backref='channel', lazy='dynamic')

    def __repr__(self):
        return '<Channel %r>' % self.name

    def __init__(self, name):
        self.name = name.strip()


class Message(db.Model):
    #id = db.Column('message_id', db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    created = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))

    def __repr__(self):
        return '<Message: %r by %r>' % (
            self.text, self.user.username)

    def __init__(self, text, user, channel):
        self.text = text.strip()
        self.user = user
        self.channel = channel
        self.created = datetime.utcnow()
