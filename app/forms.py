from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email

from app.models import User


class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(message="Username is required")])
    password = PasswordField(label="Password", validators=[DataRequired(message="Password is required"), Length(min=8, max=16, message="Minimum required length is 8 characteres")])
    remember_me = BooleanField(label="Remember me")
    submit = SubmitField(label="Log in")


class RegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(message="Username is required")])
    email = EmailField(label="Email", validators=[Email(), DataRequired(message="Email is required")])
    password = PasswordField(label="Password", validators=[DataRequired(message="Password is required"), Length(min=8, max=16, message="Minimum required length is 8 characteres")])
    password_check = PasswordField(label="Repeat password", validators=[DataRequired(message="Password is required"), Length(min=8, max=16, message="Minimum required length is 8 characteres"), EqualTo('password', message="Incorrect password")])
    submit = SubmitField(label="Register")
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField(label="Username")
    about_me = TextAreaField(label="About me")
    email = EmailField(label="Email", validators=[Email()])
    password = PasswordField(label="Password")
    submit = SubmitField(label="Update profile")


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class NewPostForm(FlaskForm):
    title = StringField(label="Title", validators=[DataRequired()])
    body = TextAreaField(label="Say something!", validators=[DataRequired(), Length(min=1, max=255)])
    submit = SubmitField('Create')