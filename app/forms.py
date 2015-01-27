from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(Form):
    userid = StringField(u'userid', validators=[DataRequired()])
    email = StringField(u'email', validators=[Email()])
    password = PasswordField(u'password', validators=[DataRequired()])
    repeat_password = PasswordField(u'repeat_password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    rememberme = BooleanField(u'rememberme', default=False)

class ManageForm(Form):
    email = StringField(u'email', validators=[Email()])
    password = PasswordField(u'password', validators=[DataRequired()])
    repeat_password = PasswordField(u'repeat_password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
