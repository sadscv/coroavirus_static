#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: sadscv
@time: 2020/02/10 16:29
@file: form.py

@desc: 
"""
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(Form):
    name = SelectField('学院名称', choices=[], coerce=int)
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('保持登录')
    submit = SubmitField('login')
