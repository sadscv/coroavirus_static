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
from sqlalchemy.orm import relationship, backref

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

    def verify_md5_password(self, md5):
        pass
        # if md5(self.password.strip())

class 教资考试(Base):
    __tablename__ = 'exam'
    序号 = Column(Integer, primary_key=True)
    教工单位 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    姓名 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    工号 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    是否需要隔离 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    备注 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))


class 线上教学(Base):
    __tablename__ = 'coronavrius'

    序号 = Column(Integer, primary_key=True)
    课程归属学院 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    任课教师 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    课程号 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    课程名称 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    班级名称 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    授课方式 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    # 转入线上授课日期 = Column(DateTime())
    # 结束线上授课日期 = Column(DateTime())
    线上教学方式 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    线上教学慕课平台 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    线上教学入口 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    申报原因 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    审核状态 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))

class 特殊课程安排(Base):
    __tablename__ = '特殊课程安排'

    开课学期 = Column(DateTime(), primary_key=True)
    课程管理单位 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    课程号 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'), primary_key=True)
    课程名称 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    班级号 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'), primary_key=True)
    班级名称 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    教师工号 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    教师姓名 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    周次 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    星期 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'), primary_key=True)
    节次 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'), primary_key=True)
    教室 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    备注 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    更新时间 = Column(DateTime())


class 预填报课程(Base):
    __tablename__ = 'coronavrius_old'

    序号 = Column(Integer, primary_key=True)
    课程归属学院 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    任课教师 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    课程号 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    课程名称 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    班级名称 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    授课方式 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    # 转入线上授课日期 = Column(DateTime())
    # 结束线上授课日期 = Column(DateTime())
    线上教学方式 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    线上教学慕课平台 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    线上教学入口 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    申报原因 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    审核状态 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))

class 第六周课程(Base):
    __tablename__ = 'coronavrius_6'

    序号 = Column(Integer, primary_key=True)
    课程归属学院 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    任课教师 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    课程号 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    课程名称 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    班级名称 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    授课方式 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    # 转入线上授课日期 = Column(DateTime())
    # 结束线上授课日期 = Column(DateTime())
    线上教学方式 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    线上教学慕课平台 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    线上教学入口 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    申报原因 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    审核状态 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    最后更新时间 = Column(DateTime())

class 延期课程(Base):
    __tablename__ = 'coronavrius_null'

    序号 = Column(Integer, primary_key=True)
    课程归属学院 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    任课教师 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    课程号 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    课程名称 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    班级名称 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    授课方式 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    开课周次 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    申报原因 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    是否已补课 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    补课详情 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))


class Major(Base):
    __tablename__ = 'major'
    学院 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    专业代码 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'), primary_key=True)
    专业名称 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    # teacher = relationship('在职教师', backref=backref('teacher'))

    # major = relationship('Major', backref=backref('major'))


class 在职教师(Base):
    __tablename__ = 'teacher'
    学院 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    工号 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'), primary_key=True)
    姓名 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    任教类型 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    任教专业名称 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    任教专业代码 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    # 任教专业代码 = Column(VARCHAR(2147483647), ForeignKey('Major.专业代码'))
    专业任教时间 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    是否实验技术人员 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    是否双师双能型 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    是否工程背景 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    是否具有国境外一年及以上经历 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    是否行业背景 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))

    # major = relationship('Major', backref=backref('major'))


class 外聘教师(Base):
    __tablename__ = 'tmpteacher'

    序号 = Column(Integer, primary_key=True, nullable=False)
    工号 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    姓名 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    性别 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    出生年月 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    聘任时间 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    任职状态 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    聘期 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    单位号 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    学院 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    学历 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    最高学位 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    专业技术职称 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    工作单位类别 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    承担本科教学任务 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))
    地区 = Column(VARCHAR(2147483647, 'Chinese_PRC_CI_AS'))


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

    专业师范性质 = relationship('专业师范性质', primaryjoin='专业.专业师范性质号 == 专业师范性质.专业师范性质号',
                          backref='专业S')


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
                print('valueerror, typeerror')

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
                raise ValueError(
                    self.gettext(u'Invalid Choice: could not coerce'))

    def pre_validate(self, form):
        """Validate sent keys to make sure user don't post data that is not a valid choice."""
        sent_data = set(self.data)
        valid_data = {k for k, _ in self.choices}
        invalid_keys = sent_data - valid_data
        if invalid_keys:
            raise ValueError(
                'These values are invalid {}'.format(','.join(invalid_keys)))
