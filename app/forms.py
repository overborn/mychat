from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Length, EqualTo


class LoginForm(Form):
    username = TextField('username',
        validators=[Required(), Length(min=3, max=18)])
    password = PasswordField('password',
        validators=[Required(), Length(min=8, max=18)])


class SignupForm(Form):
    username = TextField('username',
        validators=[Required(), Length(min=3, max=18)])
    password = PasswordField('password', validators=[Required(),
        Length(min=8, max=18), 
        EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('confirm')


class AddChannelForm(Form):
    name = TextField(validators=[Required()])
