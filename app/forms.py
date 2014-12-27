from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
	userid = StringField(u'userid', validators=[DataRequired()])
	password = PasswordField(u'password', validators=[DataRequired()])
	rememberme = BooleanField('rememberme', default=False)