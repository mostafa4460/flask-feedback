from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, Email

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[
        InputRequired(message="Username cannot be blank"),
        Length(min=6, max=20, message="Username has to be between 6-20 chars")
    ])
    password = PasswordField("Password", validators=[InputRequired(message="Password cannot be blank")])
    email = EmailField("Email", validators=[
        InputRequired(message="Password cannot be blank"),
        Email(message="Invalid email")
    ])
    first_name = StringField("First Name", validators=[
        InputRequired(message="First name cannot be blank"),
        Length(min=1, max=30, message="First name has to be between 1-30 chars")
    ])
    last_name = StringField("Last Name", validators=[
        InputRequired(message="Last name cannot be blank"),
        Length(min=1, max=30, message="Last name has to be between 1-30 chars")
    ])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Username cannot be blank")])
    password = PasswordField("Password", validators=[InputRequired(message="Password cannot be blank")])

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[
        InputRequired(message="Title cannot be blank"),
        Length(min=1, max=100, message="Title has to be between 1-100 chars")
    ])
    content = TextAreaField("Content", validators=[InputRequired("Content cannot be blank")])