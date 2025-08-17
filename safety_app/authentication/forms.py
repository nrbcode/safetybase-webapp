# -*- encoding: utf-8 -*-
"""
Login and registration forms
"""
from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField, BooleanField
from wtforms.validators import Email, DataRequired


class LoginForm(FlaskForm):
    username = TextAreaField('Username',
                             id='username_login',
                             validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])
    remember_me = BooleanField('Remember',
                               id='remember_login')


class CreateAccountForm(FlaskForm):
    username = TextAreaField('Username',
                             id='username_create',
                             validators=[DataRequired()])
    email = TextAreaField('Email',
                          id='email_create',
                          validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])

