#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: sadscv
@time: 2020/01/28 19:41
@file: utils.py

@desc: 
"""
from flask import g
from flask_admin.contrib.sqla import ModelView

from app.models import 专业
from manage import admin


def create_admin_view():
    admin.add_view(ModelView(专业, g.session))
