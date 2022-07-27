# from wsgiref.validate import validators
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import DataRequired, Length,Email

class ContactForm(FlaskForm):
    fullname = StringField('enter your fullname', validators=[DataRequired(message="please input your fullname"),Length(min=5)])
    email = StringField('email', validators=[Email()])
    message = TextAreaField()
    # password = PasswordField()
    submit = SubmitField()

class SignupForm(FlaskForm):
    firstname = StringField('', validators=[DataRequired(message="please input your firstname"),Length(min=4)])
    lastname = StringField('', validators=[DataRequired(message="please input your lastname"),Length(min=4)])
    email = StringField('', validators=[Email('a valid email is required')])
    password = PasswordField('you password must be more than 4 characters', validators=[DataRequired(),Length(min=5)])
   # confirm_password = PasswordField('check sure the password matches', validators=[DataRequired()])
    submit = SubmitField('submit it')



#we have to install email_validator
# pip install email_validator