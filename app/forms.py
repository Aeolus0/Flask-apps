from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo


class SignupForm(Form):
    username = StringField(u'uusername', validators=[DataRequired()])
    email = StringField(u'email', validators=[Email(), DataRequired()])
    password = PasswordField(u'password', validators=[DataRequired()])
    repeat_password = PasswordField(u'repeat_password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    rememberme = BooleanField(u'rememberme', default=False)

class ManageForm(Form):
    email = StringField(u'email', validators=[Email()])
    password = PasswordField(u'password', validators=[DataRequired()])
    repeat_password = PasswordField(u'repeat_password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])

class IndexForm(Form):
    search = StringField(u'search', default="Search Present.ly")

class MDEditor(Form):
    page_title = StringField(u'page_title', validators=[DataRequired()], default="Your page title goes here!")
    slide_type = SelectField(u'slide_type', validators=[DataRequired()], choices=[("title", "Title"), ("subtitle", "Subtitle"), ("slide", "Slide")])
    slide_content = StringField(u'slide_content', validators=[DataRequired()], default="The content for the slide goes here.")