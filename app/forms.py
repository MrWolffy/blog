# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class UserRegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    repassword = StringField('repassword', validators=[DataRequired()])
    submit = SubmitField('submit')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    submit = SubmitField('submit')


class SuggestionForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])


class EditForm(FlaskForm):
    username = StringField('username', validators=None)
    password = StringField('password', validators=None)
    repassword = StringField('repassword', validators=None)
    sign = TextAreaField('sign', validators=None)
    submit = SubmitField('提交更改')


