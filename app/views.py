# -*- coding: utf-8 -*-
from app import app, db, lm, socketio
from models import User, Message, Channel
from forms import SignupForm, LoginForm, AddChannelForm
from flask import render_template, flash, g, redirect, url_for, request
from flask.ext.login import login_user, logout_user, current_user, login_required
import random, re, hashlib, string
from flask.ext.socketio import emit, join_room, leave_room

from gevent import monkey
monkey.patch_all()


def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))
def make_pw_hash(name, pw, salt=None):
    if not salt: salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)
def valid_pw(name, pw, h):
    return h == make_pw_hash(name, pw, h.split('|')[1])
def valid_username(username):
    return re.match(r'^[a-zA-Z0-9_-]{3,18}', username)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('main'))
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        if not valid_username(username):
            flash('Invalid username, try another one.')
            return render_template('signup.html', form=form)
        registered_user = User.query.filter_by(username=username).first()
        if registered_user:
            flash('User already exists, try another username')
            return render_template('signup.html', form=form)
        password = form.password.data
        pw = make_pw_hash(username, password)
        user = User(username, pw)
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        registered_user = User.query.filter_by(username=username).first()
        if registered_user is None or not valid_pw(
                username, password, registered_user.pw_hash):
            flash('Username or password is invalid')
            return redirect(url_for('login'))
        login_user(registered_user)
        flash('Logged in successfully')
        return redirect(request.args.get('next') or url_for('main'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    form = AddChannelForm()
    if form.validate_on_submit():
        name = form.name.data
        existing = Channel.query.filter_by(name=name).first()
        if existing is not None:
            flash('connecting to existing channel...')
            return redirect(url_for('channel', id=existing.id))
        channel = Channel(name)
        db.session.add(channel)
        db.session.commit()
        flash('Welcome to channel %s!' % name)
        return redirect(url_for('channel', id=channel.id))
    return render_template('main.html', form=form)


def get_channels(max_results, query):
    channels = Channel.query.all()
    if query != '':
        channels = Channel.query.filter(
            Channel.name.like('%' + query + '%')).all()
    if max_results > 0:
        channels = channels[:max_results]
    return channels


@app.route('/suggest_channel')
def suggest_channel():
    query = request.args['suggestion'].strip()
    channels = get_channels(10, query)
    return render_template('channel_list.html', channels=channels)


@app.route('/channel/<int:id>', methods=['GET', 'POST'])
@login_required
def channel(id):
    channel = Channel.query.get(id)
    if channel is None:
        flash('Channel is not found')
        return redirect(url_for('main'))
    g.user.channel = channel
    current_user.channel = channel
    return render_template('channel.html', channel=channel)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    emit('my response',
         {'data': "User " + current_user.username + " joined the channel"},
         room=message['room'])


@socketio.on('my event', namespace='/test')
def send_message(text):
    user = current_user
    # join_room(text['room'])
    channel = Channel.query.filter_by(name=text['room']).first()
    message = Message(text['data'], user, channel)
    db.session.add(message)
    db.session.commit()
    z = render_template('message.html', message=message)
    emit('my response', {'data': z}, room=text['room'])


@socketio.on('leave', namespace='/test')
def leave(text):
    leave_room(text['room'])
    emit('my response',
         {'data': 'User ' + current_user.username + " left the channel"},
         room=text['room'])
