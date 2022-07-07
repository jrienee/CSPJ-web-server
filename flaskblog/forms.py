from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from wtforms.fields.html5 import EmailField, DateField
from flaskblog.models import *
import sqlite3

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    # phone = StringField('Contact Number', validators=[DataRequired()])
    # birthdate = DateField('Birth Date', validators=[DataRequired()])
    # gender = SelectField('Gender', validators=[DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    # def validate_phone(self, phone):
    #     conn = sqlite3.connect('user.db')
    #     c = conn.cursor()
    #     c.execute("SELECT * FROM users WHERE phone='{}'".format(phone))
    #     user = c.fetchone()
    #     print(user)
    #     conn.commit()
    #     conn.close()
    #     if user:
    #         raise ValidationError('That phone number is taken. Please use a different one.')


    def validate_username(self,username):
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username='{}'".format(username))
        user = c.fetchone()
        print(user)
        conn.commit()
        conn.close()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self,email):
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email='{}'".format(email))
        user = c.fetchone()
        print(user)
        conn.commit()
        conn.close()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



    # def validate_phone(self, phone):
    #     user = User.query.filter_by(phone = phone.data).first()
    #     if user:
    #         raise ValidationError('That phone number is taken. Please use a different one.')
    #
    #
    # def validate_username(self,username):
    #     user = User.query.filter_by(username = username.data).first()
    #     if user:
    #         raise ValidationError('That username is taken. Please choose a different one.')
    #
    # def validate_email(self,email):
    #     user = User.query.filter_by(email = email.data).first()
    #     if user:
    #         raise ValidationError('That email is taken. Please choose a different one.')
    #

# class RegistrationForm(FlaskForm):
#     username = StringField('Username',
#                            validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password',
#                                      validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
