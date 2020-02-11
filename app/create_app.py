#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: sadscv
@time: 2020/01/28 13:32
@file: create_app.py

@desc: 
"""
from flask import Flask, g
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_admin import Admin

from app.config import config
from app.models import 专业
from app.views import main_blueprint

bootstrap = Bootstrap()
login_manager = LoginManager()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.secret_key = 'tmptoset'
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.jinja_env.filters['min'] = min
    app.jinja_env.filters['max'] = max
    bootstrap.init_app(app)
    moment.init_app(app)

    my_engine = create_engine(config[config_name].SQLALCHEMY_DATABASE_URI)
    SESSION = scoped_session(sessionmaker(bind=my_engine))


    @app.before_request
    def init_session():
        g.session = SESSION()

    @app.teardown_request
    def remove_session(exp=None):
        g.session.close()

    return app, SESSION
