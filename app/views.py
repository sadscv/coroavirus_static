#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: sadscv
@time: 2020/01/28 13:30
@file: views.py

@desc: 
"""
import re

from flask import Blueprint, g, redirect, url_for, flash, render_template, request
from flask_login import login_user, logout_user

from app.form import LoginForm
from app.models import User, Coronavirus

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET'])
def index():
    return '200'


# @main_blueprint.route('/login')
# def login():
#     user = g.session.query(User).filter(User.name == '政法学院').first()
#     print('$$$$$$$', type(user))
#     login_user(user)
#     return 'Logged in'


@main_blueprint.route('/logout')
def logout():
    logout_user()
    return 'Logged out'


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    form.name.choices = [(r.id, r.name) for r in g.session.query(User).all()]
    # form.name.choices = ['1', '2', '3']
    if form.validate_on_submit():
        user = g.session.query(User).filter_by(id=form.name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            # flash('登录成功')
            return redirect(request.args.get('next') or url_for('coronavirus.index_view'))
        flash('Invalid username or password')
    return render_template('/login.html', form=form)


@main_blueprint.route('/valid')
def valid():

    coros = g.session.query(Coronavirus).all()
    # for c in coros:
    #     print(c.线上教学方式)
    #     if re.match('')
    return '200'


@main_blueprint.route('/info')
def info():
    college = [c[0] for c in g.session.query(User.name).all()]
    # infos = [d[0] for d in g.session.query(Coronavirus.是否延期).all()]
    # infos = set(infos)
    # for i in infos:
    #     if str(i).startswith("延期"):
    #         print(i)
    # for j in infos:
    #     if str(j).startswith("其它"):
    #         print(j)

    for c in college:
        infos = g.session.query(Coronavirus).filter(Coronavirus.课程归属学院 == c).all()
        onlines = g.session.query(Coronavirus) \
            .filter(Coronavirus.课程归属学院 == c) \
            .filter(Coronavirus.是否延期.ilike('否%')).all()
        delays = g.session.query(Coronavirus) \
            .filter(Coronavirus.课程归属学院 == c) \
            .filter(Coronavirus.是否延期.ilike('延期%')).all()
        others = g.session.query(Coronavirus) \
            .filter(Coronavirus.课程归属学院 == c) \
            .filter(Coronavirus.是否延期.ilike('其它%')).all()
        print (c, len(onlines), len(delays), len(others), len(infos))

    return '200'
