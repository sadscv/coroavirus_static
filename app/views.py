#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: sadscv
@time: 2020/01/28 13:30
@file: views.py

@desc: 
"""
import re

from flask import Blueprint, g, redirect, url_for, flash, render_template, \
    request
from flask_login import login_user, logout_user
from sqlalchemy import or_, any_

from app.form import LoginForm
from app.models import User, 线上教学

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/admin', methods=['GET'])
def index():
    return '<h1>200</h1>'


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


@main_blueprint.route('/tmp')
def tmp():
    result = []
    week = '一二三四五六日'
    date = ['12', '3', '4', '5', '67', '89', '晚']
    for i in range(len(week)):
        for j in range(len(date)):
            tmp1 = str(i + 1) + '-' + str(j + 1)
            tmp2 = '周' + week[i] + '-' + date[j]
            tmp3 = (tmp2, tmp2)
            result.append(tmp3)
    print(result)
    return '200'


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
            return redirect(
                request.args.get('next') or url_for('admin_view_normal.index_view'))
        flash('Invalid username or password')
    return render_template('/login.html', form=form)


@main_blueprint.route('/valid')
def valid():
    coros = g.session.query(线上教学).all()
    # for c in coros:
    #     print(c.线上教学方式)
    #     if re.match('')
    return '200'


@main_blueprint.route('/info_live_platform')
def info_live_platform():
    college = [c[0] for c in g.session.query(User.name).all()]

    qq = g.session.query(线上教学) \
        .filter(线上教学.直播或录播软件_选填.ilike('%QQ%'))
    wechat = g.session.query(线上教学) \
        .filter(线上教学.直播或录播软件_选填.ilike('%微信%'))
    tx_meeting = g.session.query(线上教学) \
        .filter(线上教学.直播或录播软件_选填.ilike('%腾讯会议%'))
    ding = g.session.query(线上教学) \
        .filter(线上教学.直播或录播软件_选填.ilike('%钉钉%'))
    result = [qq, wechat, tx_meeting, ding]

    for c in college:
        tmp = []
        for platform in result:
            tmp.append(len(platform.filter(线上教学.课程归属学院 == c).all()))
        print(c, tmp)
    tmp = []
    for r in result:
        tmp.append(len(r.all()))
    print('合计', tmp)
    # infos = g.session.query(Coronavirus).filter(Coronavirus.课程归属学院 == c).all()

    return '200'


@main_blueprint.route('/info_platform')
def info_platform():
    college = [c[0] for c in g.session.query(User.name).all()]

    headlines = '学院 班级总数 雨课堂 超星学习通 腾讯会议 中国大学MOOC  钉钉 其它'
    print(headlines)
    for c in college:
        infos = g.session.query(线上教学).filter(
            线上教学.课程归属学院 == c).all()
        zgdxmooc = g.session.query(线上教学).filter(线上教学.线上教学慕课平台.ilike('%中国大学%'), 线上教学.课程归属学院 == c).all()
        chaoxin = g.session.query(线上教学) \
            .filter(线上教学.线上教学慕课平台.ilike('%超星%'), 线上教学.课程归属学院 == c).all()
        tencentmeeting = g.session.query(线上教学) \
            .filter(线上教学.线上教学慕课平台.ilike('%腾讯会议%'), 线上教学.课程归属学院 == c).all()
        railcourse = g.session.query(线上教学) \
            .filter(线上教学.线上教学慕课平台.ilike('%雨课堂%'), 线上教学.课程归属学院 == c).all()
        ding = g.session.query(线上教学) \
            .filter(线上教学.线上教学慕课平台.ilike('%钉钉%'), 线上教学.课程归属学院 == c).all()
        other_options = ['%学堂在线%', '其它', '无', 'QQ群', '智慧树', '学校网络']
        others = g.session.query(线上教学).filter(线上教学.课程归属学院 == c).filter(or_(*[线上教学.线上教学慕课平台.like(other) for other in other_options])).all()
        print(c, len(infos), len(railcourse), len(chaoxin),len(tencentmeeting), len(zgdxmooc), len(ding), len(others))

    # for c in college:
    #     tmp = []
    #     for platform in result:
    #         tmp.append(len(platform.filter(线上教学.课程归属学院 == c).all()))
    #     print(c, tmp)
    # tmp = []
    # for r in result:
    #     tmp.append(len(r.all()))
    # print('合计', tmp)
    #     # infos = g.session.query(Coronavirus).filter(Coronavirus.课程归属学院 == c).all()

    return '200'


@main_blueprint.route('/info')
def info():
    college = [c[0] for c in g.session.query(User.name).all()]
    # infos = [d[0] for d in g.session.query(线上教学.授课方式).all()]
    # infos = set(infos)
    # for i in infos:
    #     if str(i).startswith("延期"):
    #         print(i)
    # for j in infos:
    #     if str(j).startswith("其它"):
    #         print(j)

    headlines = '学院 班级总数 线上教学班级数 线下教学班级数 延期教学班级数 未填报班级数'
    # for h in headlines:
    print(headlines)
    for c in college:
        infos = g.session.query(线上教学).filter(
            线上教学.课程归属学院 == c).all()
        onlines = g.session.query(线上教学)\
            .filter(线上教学.课程归属学院 == c) \
            .filter(线上教学.授课方式.ilike('%线上%')).all()
        offlines = g.session.query(线上教学)\
            .filter(线上教学.课程归属学院 == c) \
            .filter(线上教学.授课方式.ilike('%线下%')).all()
        delays = g.session.query(线上教学) \
            .filter(线上教学.课程归属学院 == c) \
            .filter(线上教学.授课方式.ilike('%延期%')).all()
        others = g.session.query(线上教学)\
            .filter(线上教学.课程归属学院 == c) \
            .filter(线上教学.授课方式 == None).all()
        print(c, len(infos), len(onlines), len(offlines), len(delays),
              len(others))

    return '200'
