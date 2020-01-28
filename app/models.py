#!/usr/bin/env python
# -*- coding:utf-8 _*-
""" 
@author: sadscv
@time: 2020/01/28 14:44
@file: models.py

@desc: 
"""
from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, Integer, \
    LargeBinary, Numeric, SmallInteger, String, \
    Text, Unicode, UnicodeText
from sqlalchemy.dialects.mssql.base import BIT, MONEY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue


Base = declarative_base()
metadata = Base.metadata


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
