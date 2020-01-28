#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: sadscv
@time: 2020/01/28 13:30
@file: views.py

@desc: 
"""
from flask import Blueprint, g


main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET'])
def index():
    return '200'
