# coding: utf-8
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


class 专业目录(Base):
    __tablename__ = '\u4e13\u4e1a\u76ee\u5f55'

    专业目录号 = Column(String(8, 'Chinese_PRC_CI_AS'), primary_key=True)
    专业目录名称 = Column(String(40, 'Chinese_PRC_CI_AS'), nullable=False, unique=True)
    专业科类号 = Column(ForeignKey('专业科类.专业科类号'), nullable=False)
    单位号 = Column(String(8, 'Chinese_PRC_CI_AS'))
    领衔教师号 = Column(String(10, 'Chinese_PRC_CI_AS'))
    设立时间 = Column(DateTime, nullable=False)
    学制年限号 = Column(ForeignKey('学制年限.学制年限号'), nullable=False)
    学历号 = Column(ForeignKey('学历.学历号'), nullable=False)
    学位门类号 = Column(String(2, 'Chinese_PRC_CI_AS'), nullable=False)
    毕业最低学分 = Column(Integer, nullable=False)
    培养目标 = Column(String(800, 'Chinese_PRC_CI_AS'))
    培养要求 = Column(String(1600, 'Chinese_PRC_CI_AS'))
    方向介绍 = Column(String(800, 'Chinese_PRC_CI_AS'))
    主干学科 = Column(String(100, 'Chinese_PRC_CI_AS'))
    相近专业 = Column(String(200, 'Chinese_PRC_CI_AS'))
    审批文号 = Column(String(40, 'Chinese_PRC_CI_AS'))
    目录类别 = Column(String(2, 'Chinese_PRC_CI_AS'))
    生均经费 = Column(Integer)
    综评否 = Column(BIT)
    一般知识 = Column(Unicode(600))
    专业知识 = Column(Unicode(600))
    一般能力 = Column(Unicode(600))
    专业能力 = Column(Unicode(600))
    一般素养 = Column(Unicode(600))
    专业素养 = Column(Unicode(600))
    培养大纲 = Column(Unicode(10))
    实现矩阵 = Column(Unicode(10))

    专业科类 = relationship('专业科类', primaryjoin='专业目录.专业科类号 == 专业科类.专业科类号', backref='专业目录S')
    学制年限 = relationship('学制年限', primaryjoin='专业目录.学制年限号 == 学制年限.学制年限号', backref='专业目录S')
    学历 = relationship('学历', primaryjoin='专业目录.学历号 == 学历.学历号', backref='专业目录S')


class 专业科类(Base):
    __tablename__ = '\u4e13\u4e1a\u79d1\u7c7b'

    专业科类号 = Column(String(8, 'Chinese_PRC_CI_AS'), primary_key=True)
    专业科类名称 = Column(String(40, 'Chinese_PRC_CI_AS'), nullable=False)
    专业门类号 = Column(ForeignKey('专业门类.专业门类号'))

    专业门类 = relationship('专业门类', primaryjoin='专业科类.专业门类号 == 专业门类.专业门类号', backref='专业科类S')


class 专业门类(Base):
    __tablename__ = '\u4e13\u4e1a\u95e8\u7c7b'

    专业门类号 = Column(String(2, 'Chinese_PRC_CI_AS'), primary_key=True)
    专业门类名称 = Column(String(20, 'Chinese_PRC_CI_AS'))


class 单位(Base):
    __tablename__ = '\u5355\u4f4d'

    单位号 = Column(String(8, 'Chinese_PRC_CI_AS'), primary_key=True)
    单位名称 = Column(Unicode(30), unique=True)
    单位性质号 = Column(ForeignKey('单位性质.单位性质号'))
    单位简称 = Column(String(10, 'Chinese_PRC_CI_AS'))
    密码 = Column(String(20, 'Chinese_PRC_CI_AS'))
    教材费结余 = Column(Unicode(10))
    部门编号 = Column(Unicode(10))

    单位性质 = relationship('单位性质', primaryjoin='单位.单位性质号 == 单位性质.单位性质号', backref='单位S')


class 单位性质(Base):
    __tablename__ = '\u5355\u4f4d\u6027\u8d28'

    单位性质号 = Column(Unicode(10), primary_key=True)
    单位性质 = Column(Unicode(20))
    单位性质说明 = Column(Unicode(100))


class 学制年限(Base):
    __tablename__ = '\u5b66\u5236\u5e74\u9650'

    学制年限号 = Column(Unicode(10), primary_key=True)
    学制年限 = Column(Unicode(50))


class 学历(Base):
    __tablename__ = '\u5b66\u5386'

    学历号 = Column(Unicode(10), primary_key=True)
    学历 = Column(Unicode(50))


class 学期(Base):
    __tablename__ = '\u5b66\u671f'

    开学日期 = Column(DateTime, primary_key=True)
    学期名称 = Column(Unicode(30))
    放假日期 = Column(DateTime)
    当前学期否 = Column(String(1, 'Chinese_PRC_CI_AS'), nullable=False)


class 年级(Base):
    __tablename__ = '\u5e74\u7ea7'

    年级号 = Column(DateTime, primary_key=True)
    年级名称 = Column(Unicode(50))


class 开课合班(Base):
    __tablename__ = '\u5f00\u8bfe\u5408\u73ed'

    开课时间 = Column(ForeignKey('学期.开学日期'), primary_key=True, nullable=False)
    课程号 = Column(ForeignKey('课程.课程号'), primary_key=True, nullable=False)
    班级号 = Column(ForeignKey('班级.班级号'), primary_key=True, nullable=False)
    合班号 = Column(ForeignKey('班级.班级号'), nullable=False)
    教号 = Column(ForeignKey('教工.教号'), nullable=False)
    多媒体否 = Column(String(1, 'Chinese_PRC_CI_AS'))
    双语否 = Column(String(1, 'Chinese_PRC_CI_AS'))

    班级 = relationship('班级', primaryjoin='开课合班.合班号 == 班级.班级号', backref='班级_开课合班S')
    学期 = relationship('学期', primaryjoin='开课合班.开课时间 == 学期.开学日期', backref='开课合班S')
    教工 = relationship('教工', primaryjoin='开课合班.教号 == 教工.教号', backref='开课合班S')
    班级1 = relationship('班级', primaryjoin='开课合班.班级号 == 班级.班级号', backref='班级_开课合班S_0')
    课程 = relationship('课程', primaryjoin='开课合班.课程号 == 课程.课程号', backref='开课合班S')


class 开课安排(Base):
    __tablename__ = '\u5f00\u8bfe\u5b89\u6392'
    __table_args__ = (
        Index('IX_\u5f00\u8bfe\u5b89\u6392', '\u73ed\u7ea7\u53f7', '\u661f\u671f\u53f7', '\u8282\u6b21\u53f7',
              '\u5f00\u8bfe\u65f6\u95f4', '\u65f6\u6001'),
        Index('IX_\u5f00\u8bfe\u5b89\u6392_1', '\u5f00\u8bfe\u65f6\u95f4', '\u6559\u53f7', '\u661f\u671f\u53f7',
              '\u8282\u6b21\u53f7', '\u65f6\u6001'),
        Index('IX_\u5f00\u8bfe\u5b89\u6392_2', '\u5f00\u8bfe\u65f6\u95f4', '\u6559\u5ba4\u53f7', '\u661f\u671f\u53f7',
              '\u8282\u6b21\u53f7', '\u65f6\u6001')
    )

    开课时间 = Column(ForeignKey('学期.开学日期'), primary_key=True, nullable=False)
    课程号 = Column(ForeignKey('课程.课程号'), primary_key=True, nullable=False)
    班级号 = Column(ForeignKey('班级.班级号'), primary_key=True, nullable=False)
    星期号 = Column(ForeignKey('星期.星期号'), primary_key=True, nullable=False)
    节次号 = Column(ForeignKey('节次.节次号'), primary_key=True, nullable=False)
    教号 = Column(ForeignKey('教工.教号'), nullable=False)
    教室号 = Column(ForeignKey('教室.教室号'), nullable=False)
    周次号 = Column(String(2, 'Chinese_PRC_CI_AS'))
    实验课否 = Column(String(1, 'Chinese_PRC_CI_AS'), nullable=False)
    时态 = Column(String(1, 'Chinese_PRC_CI_AS'))

    学期 = relationship('学期', primaryjoin='开课安排.开课时间 == 学期.开学日期', backref='开课安排S')
    教工 = relationship('教工', primaryjoin='开课安排.教号 == 教工.教号', backref='开课安排S')
    教室 = relationship('教室', primaryjoin='开课安排.教室号 == 教室.教室号', backref='开课安排S')
    星期 = relationship('星期', primaryjoin='开课安排.星期号 == 星期.星期号', backref='开课安排S')
    班级 = relationship('班级', primaryjoin='开课安排.班级号 == 班级.班级号', backref='开课安排S')
    节次 = relationship('节次', primaryjoin='开课安排.节次号 == 节次.节次号', backref='开课安排S')
    课程 = relationship('课程', primaryjoin='开课安排.课程号 == 课程.课程号', backref='开课安排S')


class 开课拆班(Base):
    __tablename__ = '\u5f00\u8bfe\u62c6\u73ed'

    开课时间 = Column(ForeignKey('学期.开学日期'), primary_key=True, nullable=False)
    课程号 = Column(ForeignKey('课程.课程号'), primary_key=True, nullable=False)
    拆班号 = Column(ForeignKey('班级.班级号'), primary_key=True, nullable=False)
    班级号 = Column(ForeignKey('班级.班级号'), primary_key=True, nullable=False)
    教号 = Column(ForeignKey('教工.教号'), nullable=False)
    拆班状态 = Column(String(1, 'Chinese_PRC_CI_AS'), nullable=False)
    授课人数 = Column(SmallInteger)
    班级容量 = Column(SmallInteger)
    极限容量 = Column(SmallInteger)
    选课总人数 = Column(SmallInteger)
    期望人数 = Column(SmallInteger)
    调前授课人数 = Column(SmallInteger)
    调前总人数 = Column(SmallInteger)
    调前班级号 = Column(String(20, 'Chinese_PRC_CI_AS'))
    教材ISBN = Column(ForeignKey('教材.教材ISBN'))
    辅助教材否 = Column(String(1, 'Chinese_PRC_CI_AS'))
    双语否 = Column(String(1, 'Chinese_PRC_CI_AS'))
    多媒体否 = Column(String(1, 'Chinese_PRC_CI_AS'))
    开课说明 = Column(String(20, 'Chinese_PRC_CI_AS'))
    教室类型号 = Column(ForeignKey('教室类型.教室类型号'))
    排课说明 = Column(String(40, 'Chinese_PRC_CI_AS'))
    插入时间 = Column(DateTime, server_default=FetchedValue())
    考试人数 = Column(SmallInteger)
    试卷平均分 = Column(Numeric(4, 2))
    试卷标准差 = Column(Numeric(5, 3))
    阿尔法信度 = Column(Numeric(5, 3))
    分半矫正信度 = Column(Numeric(5, 3))
    试卷总体分析 = Column(String(100, 'Chinese_PRC_CI_AS'))
    试题分析 = Column(String(200, 'Chinese_PRC_CI_AS'))
    问题与对策 = Column(String(100, 'Chinese_PRC_CI_AS'))
    题量 = Column(Integer)
    提交平时否 = Column(String(1, 'Chinese_PRC_CI_AS'))
    提交期末否 = Column(String(1, 'Chinese_PRC_CI_AS'))
    分析试卷否 = Column(String(1, 'Chinese_PRC_CI_AS'))
    性别限定 = Column(String(2, 'Chinese_PRC_CI_AS'))
    课程性质号 = Column(ForeignKey('课程性质.课程性质号'))
    满意度和 = Column(Float(53))
    评星人数 = Column(Float(53))

    学期 = relationship('学期', primaryjoin='开课拆班.开课时间 == 学期.开学日期', backref='开课拆班S')
    班级 = relationship('班级', primaryjoin='开课拆班.拆班号 == 班级.班级号', backref='班级_开课拆班S')
    教工 = relationship('教工', primaryjoin='开课拆班.教号 == 教工.教号', backref='开课拆班S')
    教室类型 = relationship('教室类型', primaryjoin='开课拆班.教室类型号 == 教室类型.教室类型号', backref='开课拆班S')
    教材 = relationship('教材', primaryjoin='开课拆班.教材ISBN == 教材.教材ISBN', backref='开课拆班S')
    班级1 = relationship('班级', primaryjoin='开课拆班.班级号 == 班级.班级号', backref='班级_开课拆班S_0')
    课程 = relationship('课程', primaryjoin='开课拆班.课程号 == 课程.课程号', backref='开课拆班S')
    课程性质 = relationship('课程性质', primaryjoin='开课拆班.课程性质号 == 课程性质.课程性质号', backref='开课拆班S')


class 开课计划(Base):
    __tablename__ = '\u5f00\u8bfe\u8ba1\u5212'

    开课时间 = Column(DateTime, primary_key=True, nullable=False)
    课程号 = Column(ForeignKey('课程.课程号'), primary_key=True, nullable=False)
    班级号 = Column(ForeignKey('班级.班级号'), primary_key=True, nullable=False)
    开课状态 = Column(String(1, 'Chinese_PRC_CI_AS'), nullable=False)
    课程性质号 = Column(String(2, 'Chinese_PRC_CI_AS'), nullable=False)
    组班状态 = Column(String(1, 'Chinese_PRC_CI_AS'))
    周次分布号 = Column(String(2, 'Chinese_PRC_CI_AS'))
    相关实验课程号 = Column(Unicode(14))
    实践总学时 = Column(SmallInteger)
    课堂总学时 = Column(SmallInteger)
    周课堂学时 = Column(SmallInteger)
    周实验学时 = Column(SmallInteger)
    考试方式号 = Column(String(1, 'Chinese_PRC_CI_AS'))
    试卷存放单位号 = Column(String(8, 'Chinese_PRC_CI_AS'))
    试卷归档状态 = Column(String(12, 'Chinese_PRC_CI_AS'))
    教材ISBN = Column(String(15, 'Chinese_PRC_CI_AS'))
    教号 = Column(ForeignKey('教工.教号'))
    授课人数 = Column(SmallInteger)
    班级容量 = Column(SmallInteger)
    选课总人数 = Column(SmallInteger)
    变更类别 = Column(String(8, 'Chinese_PRC_CI_AS'))
    变更说明 = Column(String(20, 'Chinese_PRC_CI_AS'))
    排课说明 = Column(String(100, 'Chinese_PRC_CI_AS'))
    开课计划指定教室 = Column(String(10, 'Chinese_PRC_CI_AS'))
    开课计划指定教室类型号 = Column(SmallInteger)
    开始节次 = Column(String(1, 'Chinese_PRC_CI_AS'))
    结束节次 = Column(String(1, 'Chinese_PRC_CI_AS'))
    开始星期 = Column(String(1, 'Chinese_PRC_CI_AS'))
    结束星期 = Column(String(1, 'Chinese_PRC_CI_AS'))
    排课否 = Column(String(1, 'Chinese_PRC_CI_AS'))
    年级号 = Column(DateTime)
    专业号 = Column(Unicode(10))
    开课顺序号 = Column(Unicode(10))
    双语否 = Column(String(1, 'Chinese_PRC_CI_AS'))
    多媒体否 = Column(String(1, 'Chinese_PRC_CI_AS'))
    组班说明 = Column(String(200, 'Chinese_PRC_CI_AS'))
    组班名称 = Column(String(200, 'Chinese_PRC_CI_AS'))
    插入时间 = Column(DateTime, server_default=FetchedValue())
    辅助教材否 = Column(String(1, 'Chinese_PRC_CI_AS'))

    教工 = relationship('教工', primaryjoin='开课计划.教号 == 教工.教号', backref='开课计划S')
    班级 = relationship('班级', primaryjoin='开课计划.班级号 == 班级.班级号', backref='开课计划S')
    课程 = relationship('课程', primaryjoin='开课计划.课程号 == 课程.课程号', backref='开课计划S')


class 教学区(Base):
    __tablename__ = '\u6559\u5b66\u533a'

    教学区号 = Column(String(2, 'Chinese_PRC_CI_AS'), primary_key=True)
    教学区名称 = Column(String(20, 'Chinese_PRC_CI_AS'))


class 教室(Base):
    __tablename__ = '\u6559\u5ba4'

    教室号 = Column(String(12, 'Chinese_PRC_CI_AS'), primary_key=True)
    教室类型号 = Column(ForeignKey('教室类型.教室类型号'), nullable=False)
    教室定员 = Column(SmallInteger, nullable=False)
    教室地点 = Column(String(12, 'Chinese_PRC_CI_AS'))
    教学区号 = Column(ForeignKey('教学区.教学区号'), nullable=False)
    专用否 = Column(String(1, 'Chinese_PRC_CI_AS'))
    考试否 = Column(String(1, 'Chinese_PRC_CI_AS'))
    使用优先级 = Column(SmallInteger)
    教室使用说明 = Column(String(50, 'Chinese_PRC_CI_AS'))

    教学区 = relationship('教学区', primaryjoin='教室.教学区号 == 教学区.教学区号', backref='教室S')
    教室类型 = relationship('教室类型', primaryjoin='教室.教室类型号 == 教室类型.教室类型号', backref='教室S')


class 教室类型(Base):
    __tablename__ = '\u6559\u5ba4\u7c7b\u578b'

    教室类型号 = Column(SmallInteger, primary_key=True)
    教室类型 = Column(String(20, 'Chinese_PRC_CI_AS'))


class 教工(Base):
    __tablename__ = '\u6559\u5de5'

    教号 = Column(String(10, 'Chinese_PRC_CI_AS'), primary_key=True)
    姓名 = Column(Unicode(8), nullable=False)
    别名 = Column(Unicode(8))
    性别 = Column(String(2, 'Chinese_PRC_CI_AS'))
    单位号 = Column(ForeignKey('单位.单位号'), nullable=False)
    新单位号 = Column(String(8, 'Chinese_PRC_CI_AS'))
    科室号 = Column(String(10, 'Chinese_PRC_CI_AS'))
    从事专业目录号 = Column(ForeignKey('专业目录.专业目录号'))
    编制号 = Column(ForeignKey('教工编制.编制号'))
    工作组号 = Column(String(2, 'Chinese_PRC_CI_AS'))
    登录时间 = Column(DateTime)
    登录IP = Column(String(20, 'Chinese_PRC_CI_AS'))
    登录次数 = Column(SmallInteger)
    登录批次号 = Column(Integer)
    密码 = Column(String(20, 'Chinese_PRC_CI_AS'))
    密码提示问题 = Column(String(20, 'Chinese_PRC_CI_AS'))
    密码提示答案 = Column(String(20, 'Chinese_PRC_CI_AS'))
    现聘职称号 = Column(String(8, 'Chinese_PRC_CI_AS'))
    现聘职称时间 = Column(DateTime)
    现评职称号 = Column(ForeignKey('教工职称.职称号'), nullable=False)
    现评职称时间 = Column(DateTime)
    新职称号 = Column(String(8, 'Chinese_PRC_CI_AS'))
    新职称时间 = Column(DateTime)
    在岗否 = Column(String(1, 'Chinese_PRC_CI_AS'))
    在职否 = Column(String(1, 'Chinese_PRC_CI_AS'))
    离岗时间 = Column(DateTime)
    挂牌状态 = Column(SmallInteger)
    导师否 = Column(String(2, 'Chinese_PRC_CI_AS'))
    导师证编号 = Column(String(20, 'Chinese_PRC_CI_AS'))
    政治面貌号 = Column(String(3, 'Chinese_PRC_CI_AS'))
    临时筛选 = Column(Unicode(8))
    临时标识 = Column(String(1, 'Chinese_PRC_CI_AS'))
    教工异动 = Column(Unicode(200))
    教工照片 = Column(LargeBinary)
    民族 = Column(String(2, 'Chinese_PRC_CI_AS'))
    籍贯 = Column(Unicode(16))
    出生地 = Column(Unicode(40))
    出生日期 = Column(DateTime)
    最高学历号 = Column(ForeignKey('教工学历.最高学历号'))
    最高学历专业 = Column(Unicode(50))
    最高学历授予时间 = Column(DateTime)
    最高学历授予单位 = Column(Unicode(60))
    最高学位号 = Column(ForeignKey('教工学位.最高学位号'), nullable=False)
    最高学位授予时间 = Column(DateTime)
    博士学位授予时间 = Column(DateTime)
    硕士学位授予时间 = Column(DateTime)
    学士学位授予时间 = Column(DateTime)
    职务号 = Column(ForeignKey('教工职务.职务号'))
    曾任职务 = Column(Unicode(70))
    任现职时间 = Column(DateTime)
    身份证号 = Column(Unicode(18))
    健康状况 = Column(Unicode(60))
    婚姻状况 = Column(Unicode(50))
    职务工资额 = Column(Float(24))
    职务工资档次 = Column(Unicode(8))
    级别工资额 = Column(Float(24))
    级别工资档次 = Column(Unicode(8))
    入校时间 = Column(DateTime)
    入校前单位 = Column(Unicode(20))
    参加工作单位 = Column(Unicode(20))
    参加工作时间 = Column(DateTime)
    入党时间 = Column(DateTime)
    转正时间 = Column(DateTime)
    入团时间 = Column(DateTime)
    参加民主党派情况 = Column(Unicode(200))
    参加民主党派时间 = Column(DateTime)
    宗教信仰 = Column(Unicode(50))
    参加社会团体情况 = Column(Unicode(200))
    参加学术团体情况 = Column(Unicode(200))
    最高军警衔 = Column(Unicode(20))
    掌握外语情况 = Column(Unicode(100))
    评初级职称时间 = Column(DateTime)
    评中级职称时间 = Column(DateTime)
    评副高职称时间 = Column(DateTime)
    评正高职称时间 = Column(DateTime)
    县区号 = Column(Unicode(8))
    邮政编码 = Column(Unicode(6))
    家庭住址 = Column(Unicode(50))
    住房面积 = Column(Float(24))
    电子邮件 = Column(Unicode(30))
    家庭电话 = Column(Unicode(20))
    办公电话 = Column(Unicode(20))
    手机号 = Column(Unicode(20))
    心理卫生 = Column(Unicode(50))
    身高 = Column(Float(24))
    体重 = Column(Float(24))
    体育达标 = Column(String(1, 'Chinese_PRC_CI_AS'))
    英语等级 = Column(Unicode(16))
    计算机等级 = Column(Unicode(20))
    奖励 = Column(Unicode(200))
    处分 = Column(Unicode(200))
    特长情况 = Column(Unicode(200))
    家庭出身 = Column(Unicode(6))
    本人成份 = Column(Unicode(6))
    是否商品粮 = Column(String(1, 'Chinese_PRC_CI_AS'))
    教师资格证号 = Column(String(17, 'Chinese_PRC_CI_AS'))
    乘车区间 = Column(Unicode(20))
    备注 = Column(UnicodeText(1073741823))
    教学简介 = Column(UnicodeText(1073741823))
    监考否 = Column(String(1, 'Chinese_PRC_CI_AS'))
    监考限次 = Column(SmallInteger)
    固化状态 = Column(String(3, 'Chinese_PRC_CI_AS'))
    岗位资格 = Column(String(3, 'Chinese_PRC_CI_AS'))
    主讲资格 = Column(String(3, 'Chinese_PRC_CI_AS'))
    行业经历否 = Column(String(2, 'Chinese_PRC_CI_AS'))
    行业经历 = Column(String(60, 'Chinese_PRC_CI_AS'))
    学科背景 = Column(String(2, 'Chinese_PRC_CI_AS'))
    岗前培训 = Column(String(3, 'Chinese_PRC_CI_AS'))
    高层次人才级别 = Column(String(4, 'Chinese_PRC_CI_AS'))
    高层次人才称号 = Column(String(40, 'Chinese_PRC_CI_AS'))

    专业目录 = relationship('专业目录', primaryjoin='教工.从事专业目录号 == 专业目录.专业目录号', backref='教工S')
    单位 = relationship('单位', primaryjoin='教工.单位号 == 单位.单位号', backref='教工S')
    教工学位 = relationship('教工学位', primaryjoin='教工.最高学位号 == 教工学位.最高学位号', backref='教工S')
    教工学历 = relationship('教工学历', primaryjoin='教工.最高学历号 == 教工学历.最高学历号', backref='教工S')
    教工职称 = relationship('教工职称', primaryjoin='教工.现评职称号 == 教工职称.职称号', backref='教工S')
    教工编制 = relationship('教工编制', primaryjoin='教工.编制号 == 教工编制.编制号', backref='教工S')
    教工职务 = relationship('教工职务', primaryjoin='教工.职务号 == 教工职务.职务号', backref='教工S')


class 教工学位(Base):
    __tablename__ = '\u6559\u5de5\u5b66\u4f4d'

    最高学位号 = Column(Unicode(8), primary_key=True)
    最高学位 = Column(Unicode(40))
    最高学位说明 = Column(Unicode(80))
    学位等级 = Column(String(1, 'Chinese_PRC_CI_AS'))


class 教工学历(Base):
    __tablename__ = '\u6559\u5de5\u5b66\u5386'

    最高学历号 = Column(Unicode(8), primary_key=True)
    最高学历 = Column(Unicode(40))
    最高学历说明 = Column(Unicode(80))


class 教工编制(Base):
    __tablename__ = '\u6559\u5de5\u7f16\u5236'

    编制号 = Column(String(10, 'Chinese_PRC_CI_AS'), primary_key=True)
    编制名称 = Column(String(28, 'Chinese_PRC_CI_AS'))
    专任教师否 = Column(BIT, server_default=FetchedValue())
    编制名称说明 = Column(String(50, 'Chinese_PRC_CI_AS'))


class 教工职务(Base):
    __tablename__ = '\u6559\u5de5\u804c\u52a1'

    职务号 = Column(Unicode(8), primary_key=True)
    职务 = Column(Unicode(40))
    职务说明 = Column(Unicode(80))


class 教工职称(Base):
    __tablename__ = '\u6559\u5de5\u804c\u79f0'

    职称号 = Column(String(8, 'Chinese_PRC_CI_AS'), primary_key=True)
    职称 = Column(Unicode(50))
    职称说明 = Column(Unicode(80))
    职称等级 = Column(String(1, 'Chinese_PRC_CI_AS'))


class 教材(Base):
    __tablename__ = '\u6559\u6750'

    教材ISBN = Column(String(15, 'Chinese_PRC_CI_AS'), primary_key=True)
    教材名称标识 = Column(String(60, 'Chinese_PRC_CI_AS'), unique=True)
    教材名称 = Column(String(60, 'Chinese_PRC_CI_AS'), nullable=False)
    单价 = Column(MONEY, nullable=False, server_default=FetchedValue())
    库存量 = Column(Integer, nullable=False, server_default=FetchedValue())
    作者教号 = Column(Unicode(20))
    作者 = Column(String(16, 'Chinese_PRC_CI_AS'))
    协作者 = Column(String(32, 'Chinese_PRC_CI_AS'))
    出版社名称 = Column(String(40, 'Chinese_PRC_CI_AS'))
    出版时间 = Column(String(20, 'Chinese_PRC_CI_AS'))
    版次 = Column(Integer)
    是否继续出版 = Column(String(1, 'Chinese_PRC_CI_AS'))
    教材简介 = Column(String(1000, 'Chinese_PRC_CI_AS'))
    主题词 = Column(String(20, 'Chinese_PRC_CI_AS'))
    副题词 = Column(String(20, 'Chinese_PRC_CI_AS'))
    开本 = Column(String(4, 'Chinese_PRC_CI_AS'))
    页数 = Column(SmallInteger)
    封面图 = Column(LargeBinary)
    中图分类号 = Column(String(10, 'Chinese_PRC_CI_AS'))
    专业科类号 = Column(ForeignKey('专业科类.专业科类号'))
    认证情况 = Column(String(60, 'Chinese_PRC_CI_AS'))
    质量情况 = Column(String(60, 'Chinese_PRC_CI_AS'))
    适用说明 = Column(String(100, 'Chinese_PRC_CI_AS'))
    存放位置 = Column(String(20, 'Chinese_PRC_CI_AS'))

    专业科类 = relationship('专业科类', primaryjoin='教材.专业科类号 == 专业科类.专业科类号', backref='教材S')


class 星期(Base):
    __tablename__ = '\u661f\u671f'

    星期号 = Column(String(1, 'Chinese_PRC_CI_AS'), primary_key=True)
    星期 = Column(String(10, 'Chinese_PRC_CI_AS'), nullable=False)


class 班级(Base):
    __tablename__ = '\u73ed\u7ea7'

    班级号 = Column(String(20, 'Chinese_PRC_CI_AS'), primary_key=True)
    班级名称 = Column(String(40, 'Chinese_PRC_CI_AS'), nullable=False, unique=True)
    班级性质号 = Column(ForeignKey('班级性质.班级性质号'), nullable=False)
    年级号 = Column(ForeignKey('年级.年级号'))
    班级人数 = Column(SmallInteger)
    学分制状态 = Column(SmallInteger, server_default=FetchedValue())
    辅导员信息 = Column(Unicode(100))
    开课时间 = Column(DateTime)
    备注 = Column(String(40, 'Chinese_PRC_CI_AS'))
    教学区号 = Column(ForeignKey('教学区.教学区号'))
    教材费结余 = Column(MONEY)

    年级 = relationship('年级', primaryjoin='班级.年级号 == 年级.年级号', backref='班级S')
    教学区 = relationship('教学区', primaryjoin='班级.教学区号 == 教学区.教学区号', backref='班级S')
    班级性质 = relationship('班级性质', primaryjoin='班级.班级性质号 == 班级性质.班级性质号', backref='班级S')


class 班级性质(Base):
    __tablename__ = '\u73ed\u7ea7\u6027\u8d28'

    班级性质号 = Column(String(2, 'Chinese_PRC_CI_AS'), primary_key=True)
    班级性质 = Column(String(20, 'Chinese_PRC_CI_AS'))


class 科室(Base):
    __tablename__ = '\u79d1\u5ba4'

    科室号 = Column(String(10, 'Chinese_PRC_CI_AS'), primary_key=True)
    科室名称 = Column(Unicode(30), nullable=False, unique=True)
    科室类型号 = Column(ForeignKey('科室类型.科室类型号'), nullable=False)
    单位号 = Column(String(8, 'Chinese_PRC_CI_AS'), nullable=False)
    专业科类号 = Column(String(8, 'Chinese_PRC_CI_AS'), nullable=False)
    领衔教师号 = Column(String(10, 'Chinese_PRC_CI_AS'))
    电话 = Column(String(8, 'Chinese_PRC_CI_AS'))
    传真 = Column(String(8, 'Chinese_PRC_CI_AS'))

    科室类型 = relationship('科室类型', primaryjoin='科室.科室类型号 == 科室类型.科室类型号', backref='科室S')


class 科室类型(Base):
    __tablename__ = '\u79d1\u5ba4\u7c7b\u578b'

    科室类型号 = Column(String(2, 'Chinese_PRC_CI_AS'), primary_key=True)
    科室类型 = Column(String(10, 'Chinese_PRC_CI_AS'), nullable=False)
    科室类型说明 = Column(String(60, 'Chinese_PRC_CI_AS'))


class 节次(Base):
    __tablename__ = '\u8282\u6b21'

    节次号 = Column(String(1, 'Chinese_PRC_CI_AS'), primary_key=True)
    节次 = Column(String(20, 'Chinese_PRC_CI_AS'), nullable=False)
    节数 = Column(SmallInteger, nullable=False)


class 课程(Base):
    __tablename__ = '\u8bfe\u7a0b'

    课程号 = Column(String(10, 'Chinese_PRC_CI_AS'), primary_key=True)
    课程目录号 = Column(String(10, 'Chinese_PRC_CI_AS'))
    课程名称标识 = Column(Unicode(30), nullable=False)
    课程名称 = Column(Unicode(30), nullable=False)
    课程英文名称 = Column(Unicode(60))
    学分 = Column(Integer, nullable=False)
    周课堂学时 = Column(SmallInteger, nullable=False)
    科室号 = Column(ForeignKey('科室.科室号'), nullable=False)
    临时标识 = Column(String(2, 'Chinese_PRC_CI_AS'), server_default=FetchedValue())
    领衔教师号 = Column(String(10, 'Chinese_PRC_CI_AS'))
    审核教师号 = Column(String(10, 'Chinese_PRC_CI_AS'))
    周实验学时 = Column(SmallInteger)
    课堂总学时 = Column(SmallInteger)
    实践总学时 = Column(SmallInteger)
    算法号 = Column(String(2, 'Chinese_PRC_CI_AS'))
    理论课型系数 = Column(Numeric(3, 2))
    实践课型系数 = Column(Numeric(3, 2))
    理论规模系数 = Column(Integer)
    实践规模系数 = Column(Integer)
    教材ISBN = Column(String(15, 'Chinese_PRC_CI_AS'))
    教材选用说明 = Column(String(200, 'Chinese_PRC_CI_AS'))
    内容简介 = Column(Text(2147483647, 'Chinese_PRC_CI_AS'))
    适用对象 = Column(String(50, 'Chinese_PRC_CI_AS'))
    开课学期 = Column(String(1, 'Chinese_PRC_CI_AS'), server_default=FetchedValue())
    先修课程号 = Column(String(10, 'Chinese_PRC_CI_AS'))
    先修课程说明 = Column(String(200, 'Chinese_PRC_CI_AS'))
    学习要求 = Column(String(200, 'Chinese_PRC_CI_AS'))
    课程目标 = Column(String(800, 'Chinese_PRC_CI_AS'))
    教学要求 = Column(Unicode(200))
    考核方式说明 = Column(Unicode(100))
    课程教学历史 = Column(Unicode(400))
    课程教改情况 = Column(Unicode(400))
    参考书目 = Column(Unicode(200))
    课程资源超链接 = Column(Unicode(200))
    附件 = Column(Unicode(200))
    学费课程类别号 = Column(String(2, 'Chinese_PRC_CI_AS'))
    课程类别号 = Column(String(2, 'Chinese_PRC_CI_AS'))
    辅助教材否 = Column(String(1, 'Chinese_PRC_CI_AS'))
    bynumeric = Column(Float(24))
    bytext = Column(String(50, 'Chinese_PRC_CI_AS'))
    考试方式号 = Column(String(1, 'Chinese_PRC_CI_AS'))
    课程大纲能编辑否 = Column(Integer)
    课程星级 = Column(String(1, 'Chinese_PRC_CI_AS'))

    科室 = relationship('科室', primaryjoin='课程.科室号 == 科室.科室号', backref='课程S')


class 课程性质(Base):
    __tablename__ = '\u8bfe\u7a0b\u6027\u8d28'

    课程性质号 = Column(String(2, 'Chinese_PRC_CI_AS'), primary_key=True)
    课程性质 = Column(String(20, 'Chinese_PRC_CI_AS'))
    课程基数 = Column(Float(24))
    课程系数 = Column(Float(24))
    课程性质英文 = Column(String(20, 'Chinese_PRC_CI_AS'))
