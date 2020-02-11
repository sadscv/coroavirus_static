#!/usr/bin/env python
# -*- coding:utf-8 _*-
""" 
@author: sadscv
@time: 2020/01/28 14:44
@file: models.py

@desc: 
"""
from flask_login import UserMixin
from sqlalchemy import Column, DateTime, VARCHAR, ForeignKey, Integer, \
    String, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class User(Base, UserMixin):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(50, 'Chinese_PRC_CI_AS'))
    password = Column(VARCHAR(50, 'Chinese_PRC_CI_AS'))
    placeholder1 = Column(VARCHAR(50, 'Chinese_PRC_CI_AS'))

    def verify_password(self, password):
        if self.password.strip() == str(password).strip():
            return True
        return False


class Coronavirus(Base):
    __tablename__ = 'coronavrius'

    序号 = Column(Integer, primary_key=True)
    课程归属学院 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    任课教师 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    课程号 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    课程名称 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    班级名称 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    线上教学方式 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    慕课平台 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    直播_录播软件_选填_ = Column('\u76f4\u64ad\u3001\u5f55\u64ad\u8f6f\u4ef6\uff08\u9009\u586b\uff09',
                         VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    是否延期 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))


class 专业(Base):
    __tablename__ = '\u4e13\u4e1a'

    专业号 = Column(String(10, 'Chinese_PRC_CI_AS'), primary_key=True)
    专业名称 = Column(Unicode(30), nullable=False, unique=True)
    专业简称 = Column(String(16, 'Chinese_PRC_CI_AS'))
    专业师范性质号 = Column(ForeignKey('专业师范性质.专业师范性质号'), nullable=False)
    设立时间 = Column(DateTime)

    专业师范性质 = relationship('专业师范性质', primaryjoin='专业.专业师范性质号 == 专业师范性质.专业师范性质号', backref='专业S')


class 专业师范性质(Base):
    __tablename__ = '\u4e13\u4e1a\u5e08\u8303\u6027\u8d28'

    专业师范性质号 = Column(Unicode(10), primary_key=True)
    专业师范性质 = Column(Unicode(20))
    专业师范性质说明 = Column(Unicode(100))

# from flask_admin.contrib.sqla import ModelView
# admin.add_view(ModelView(专业, g.session))
