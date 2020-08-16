#!/usr/bin/env python
# -*- coding:utf-8 _*-
""" 
@author: sadscv
@time: 2020/01/28 14:44
@file: models.py

@desc: 
"""
import re

from flask_admin.form import Select2Field
from flask_login import UserMixin
from sqlalchemy import Column, DateTime, VARCHAR, ForeignKey, Integer, \
    String, Unicode, Index
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
    直播或录播软件_选填 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    是否延期 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))


class Normal(Base):
    __tablename__ = 'normal'

    序号 = Column(Integer, primary_key=True)
    课程归属学院 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    任课教师 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    课程号 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    课程名称 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    班级号 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    班级名称 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    线上开课 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    增补时段 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    是否转入线下 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    其它备注 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))


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


class MultipleSelect2Field(Select2Field):
    """Extends select2 field to make it work with postgresql arrays and using choices.

    It is far from perfect and it should be tweaked it a bit more.
    """

    def iter_choices(self):
        """Iterate over choices especially to check if one of the values is selected."""
        if self.allow_blank:
            yield (u'__None', self.blank_text, self.data is None)

        for value, label in self.choices:
            yield (value, label, value in self.data)
            # yield (value, label, self.coerce(value) in self.data)

    def process_data(self, value):
        """This is called when you create the form with existing data."""
        if value is None:
            self.data = []
        else:
            patten = '（2）爱课程（中国大学MOOC）'
            # if re.search(patten, value):
            #     print ('#########', value, value)
            try:
                self.data = value
                # self.data = [self.coerce(value) for value in value]
            except (ValueError, TypeError):
                self.data = [value]
                print ('valueerror, typeerror')

    def process_formdata(self, valuelist):
        """Process posted data."""
        if not valuelist:
            return

        if valuelist[0] == '__None':
            self.data = []
        else:
            try:
                self.data = [value for value in valuelist]
                # self.data = [self.coerce(value) for value in valuelist]
            except ValueError:
                raise ValueError(self.gettext(u'Invalid Choice: could not coerce'))

    def pre_validate(self, form):
        """Validate sent keys to make sure user don't post data that is not a valid choice."""
        sent_data = set(self.data)
        valid_data = {k for k, _ in self.choices}
        invalid_keys = sent_data - valid_data
        if invalid_keys:
            raise ValueError('These values are invalid {}'.format(','.join(invalid_keys)))
