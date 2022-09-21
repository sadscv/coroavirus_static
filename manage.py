#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: sadscv
@time: 2019/09/26 21:18
@file: manage.py

@desc: 
"""
import datetime
import os

import wtforms
from flask import url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel
from flask_login import LoginManager, current_user
from flask_marshmallow import Marshmallow
from flask_migrate import MigrateCommand
from flask_script import Manager, Server
from flask_script import Shell
from werkzeug.utils import redirect

from app.create_app import create_app
from app.models import 线上教学, User, Normal, 在职教师, \
    外聘教师, 延期课程, 预填报课程, 特殊课程安排, 第六周课程
from app.views import main_blueprint

app, SESSION = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
manager = Manager(app)
ma = Marshmallow(app)
admin = Admin(app,
              name='信息收集系统',
              template_mode='bootstrap3',
              index_view=AdminIndexView(
                  # template='welcome.html',
                  template='welcome1.html',
                  url='/admin'),
              )
login = LoginManager(app)
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'

app.register_blueprint(main_blueprint)


@login.user_loader
def load_user(u_id):
    return SESSION().query(User).filter(User.id == u_id).first()


class StringField(wtforms.fields.StringField):
    def process_data(self, value):
        self.data = value or '无'


class ArrangeView(ModelView):
    form_widget_args = {
        '课程归属学院': {'readonly': True},
        '任课教师': {'readonly': True},
        '课程号': {'readonly': True},
        '课程名称': {'readonly': True},
        '班级名称': {'readonly': True}
    }


class TeacherView(ModelView):
    can_create = False
    can_delete = False
    can_edit = True
    # column_display_pk = True
    column_list = ['学院', '工号', '姓名', '任教类型', '任教专业名称', '任教专业代码', '专业任教时间'] \
        # ,'是否实验技术人员', '是否双师双能型', '是否工程背景', '是否行业背景','是否具有国境外一年及以上经历' ]
    page_size = 100
    can_export = True
    export_types = ['xlsx']

    column_searchable_list = (
        '工号', '姓名', '学院')
    form_widget_args = {
        # '学院': {'readonly': True},
        # '姓名': {'readonly': True},
        # '工号': {'readonly': True},
        'description': {
            'rows': 10,
            'style': 'color: black'
        },

        '是否实验技术人员': {
            'readonly': True
        },
        '是否双师双能型': {
            'readonly': True
        },
        '是否工程背景': {
            'readonly': True
        },
        '是否行业背景': {
            'readonly': True
        },
        '是否具有国境外一年及以上经历': {
            'readonly': True
        }
    }
    form_choices = {
        # '专业任教时间': [('2000', '2000'), ('2001', '2001'), ],
        '任教类型': [('公共课', '公共课'), ('专业课', '专业课'), ('其它教学任务', '其它教学任务'),
                 ('无任教', '无任教')],
        # '是否双师双能型': [('是', '是'), ('否', '否')],
        # '是否工程背景': [('是', '是'), ('否', '否')],
        # '是否具有国境外一年及以上经历': [('是', '是'), ('否', '否')],
        # '是否行业背景': [('是', '是'), ('否', '否')],
    }

    form_overrides = {
        '任教专业名称': StringField,
        '任教专业代码': StringField,
        '专业任教时间': StringField,
    }

    column_default_sort = '学院'
    # column_editable_list = ['任教类型', '任教专业名称', '任教专业代码', '专业任教时间', ]
    # '是否实验技术人员', '是否双师双能型', '是否工程背景', '是否具有国境外一年及以上经历', '是否行业背景'
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['学院']

    # excluded_list_columns = [# '是否实验技术人员', '是否双师双能型', '是否工程背景', '是否具有国境外一年及以上经历', '是否行业背景']

    # form_ajax_refs = {"任教专业代码": {"fields": (Major.专业代码,)}}

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))

    def get_query(self):
        print(current_user.get_id())
        college = SESSION.query(User.name).filter(
            User.id == str(current_user.get_id())).first()[0]
        if college == '教务处':
            return super(TeacherView, self).get_query()
        else:
            return super(TeacherView, self).get_query().filter(
                在职教师.学院 == college)


class TmpTeacherView(ModelView):
    can_create = True
    can_delete = True
    can_edit = True
    # column_display_pk = True
    column_list = ['学院', '工号', '姓名', '性别', '出生年月', '聘任时间',
                   '任职状态', '聘期', '单位号', '学历', '最高学位',
                   '专业技术职称', '工作单位类别', '承担本科教学任务', '地区']
    page_size = 100
    can_export = True
    export_types = ['xlsx']

    column_searchable_list = (
        '工号', '姓名', '学院')
    form_widget_args = {
        # '学院': {'readonly': True},
        # '姓名': {'readonly': True},
        # '工号': {'readonly': True},
        # 'description': {
        #     'rows': 10,
        #     'style': 'color: black'
    }
    form_choices = {
        '性别': [('男', '男'), ('女', '女')],
        '任职状态': [('在聘', '在聘'), ('当年离职', '当年离职')],
        '学历': [('大学本科', '大学本科'), ('硕士研究生', '硕士研究生'), ('博士研究生', '博士研究生'),
               ('专科及以下', '专科及以下')],
        '最高学位': [('博士', '博士'), ('硕士', '硕士'), ('学士', '学士'), ('无学位', '无学位')],
        '专业技术职称': [('教授', '教授'), ('副教授', '副教授'), ('讲师', '讲师'), ('助教', '助教'),
                   ('其他正高级', '其他正高级'), ('其他副高级', '其他副高级'),
                   ('其他中级', '其他中级'), ('其他初级', '其他初级'), ('未评级', '未评级')],
        '工作单位类别': [('行政单位', '行政单位'), ('科研单位', '科研单位'), ('高等学校', '高等学校'),
                   ('基础教育学校', '基础教育学校'),
                   ('中等职业学校', '中等职业学校'), ('特殊教育学校等机构', '特殊教育学校等机构'),
                   ('其他事业单位', '其他事业单位'),
                   ('企业公司', '企业公司'), ('部队', '部队'),
                   ('博士或博士后及其他单位', '博士或博士后及其他单位')],
        '地区': [('境内', '境内'), ('境外（国外及港澳台）', '境外（国外及港澳台）')],
        '承担本科教学任务': [('课程教学', '课程教学'), ('指导实习、毕业设计（论文）', '指导实习、毕业设计（论文）'),
                     ('课程教学及指导实习', '课程教学及指导实习'), ('毕业设计（论文）', '毕业设计（论文）'),
                     ('无', '无')]

    }
    form_args = {
        # '聘任时间': {
        #     'validators': [regexp('^(19|20)\d{2}$', message='请输入年份,如 2001 ')],
        # },
        # '聘期': {
        #     'validators': [
        #         regexp('^1000$|^(\d|[1-9]\d\d)$', message='聘期以月为单位')],
    }
    # }

    column_default_sort = '学院'
    # column_editable_list = ['学院','工号', '性别', '出生年月', '聘任时间', '任职状态', '聘期',
    #                         '单位号', '学历', '最高学位', '专业技术职称',
    #                         '工作单位类别', '承担本科教学任务', '地区']
    create_modal = True
    edit_modal = True

    # form_excluded_columns = ['学院']

    # form_ajax_refs = {"任教专业代码": {"fields": (Major.专业代码,)}}

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))

    def get_query(self):
        print(current_user.get_id())
        college = SESSION.query(User.name).filter(
            User.id == str(current_user.get_id())).first()[0]
        if college == '教务处':
            return super(TmpTeacherView, self).get_query()
        else:
            return super(TmpTeacherView, self).get_query().filter(
                外聘教师.学院 == college)


class NormalView(ModelView):
    can_create = False
    can_delete = False
    column_display_pk = True
    column_list = ['序号', '课程归属学院', '任课教师', '课程号', '课程名称', '班级号', '班级名称', '线上开课',
                   '增补时段', '其它备注', '申报原因']
    # column_list = ['序号', '课程归属学院', '任课教师', '课程号', '课程名称', '班级号', '班级名称', '线上开课',
    #                '是否转入线下', '增补时段', '其它备注']
    column_sortable_list = (
        '序号', '课程归属学院', '任课教师', '课程名称', '课程号', '班级名称', '线上开课')
    column_searchable_list = (
        '申报原因')
    column_default_sort = '序号'
    page_size = 50
    can_export = True
    export_types = ['xlsx']

    form_widget_args = {
        '课程归属学院': {'readonly': True},
        '任课教师': {'readonly': True},
        '课程号': {'readonly': True},
        '课程名称': {'readonly': True},
        '班级号': {'readonly': True},
        '班级名称': {'readonly': True},
        '是否转入线下': {'readonly': True},
    }

    form_overrides = dict(
        # 增补时段=MultipleSelect2Field,
    )
    choices_tuple_add = (
        ('周一-12', '周一-12'), ('周一-3', '周一-3'), ('周一-4', '周一-4'),
        ('周一-5', '周一-5'), ('周一-67', '周一-67'), ('周一-89', '周一-89'),
        ('周一-晚', '周一-晚'),
        ('周二-12', '周二-12'), ('周二-3', '周二-3'), ('周二-4', '周二-4'),
        ('周二-5', '周二-5'), ('周二-67', '周二-67'), ('周二-89', '周二-89'),
        ('周二-晚', '周二-晚'),
        ('周三-12', '周三-12'), ('周三-3', '周三-3'), ('周三-4', '周三-4'),
        ('周三-5', '周三-5'), ('周三-67', '周三-67'), ('周三-89', '周三-89'),
        ('周三-晚', '周三-晚'),
        ('周四-12', '周四-12'), ('周四-3', '周四-3'), ('周四-4', '周四-4'),
        ('周四-5', '周四-5'), ('周四-67', '周四-67'), ('周四-89', '周四-89'),
        ('周四-晚', '周四-晚'),
        ('周五-12', '周五-12'), ('周五-3', '周五-3'), ('周五-4', '周五-4'),
        ('周五-5', '周五-5'), ('周五-67', '周五-67'), ('周五-89', '周五-89'),
        ('周五-晚', '周五-晚'),
        ('周六-12', '周六-12'), ('周六-3', '周六-3'), ('周六-4', '周六-4'),
        ('周六-5', '周六-5'), ('周六-67', '周六-67'), ('周六-89', '周六-89'),
        ('周六-晚', '周六-晚'),
        ('周日-12', '周日-12'), ('周日-3', '周日-3'), ('周日-4', '周日-4'),
        ('周日-5', '周日-5'), ('周日-67', '周日-67'), ('周日-89', '周日-89'),
        ('周日-晚', '周日-晚')
    )
    form_args = dict(
        增补时段=dict(render_kw=dict(multiple="multiple"),
                  choices=choices_tuple_add),
    )

    form_choices = {
        # '是否转入线下': [('转入线下', '转入线下'), ('维持线上', '维持线上'), ],
        '线上开课': [('已线上开课', '已线上开课'), ('延期开课', '延期开课'), ],
    }

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))

    def on_model_change(self, form, model, is_created):
        # form.线上教学方式.raw_data = str(form.线上教学方式.raw_data)
        if len(form.增补时段.raw_data) > 0:
            model.增补时段 = ','.join(form.增补时段.raw_data)

        # if len(form.慕课平台.raw_data) > 0:
        #     model.慕课平台 = ','.join(form.慕课平台.raw_data)
        else:
            model.增补时段 = ''

    def get_query(self):
        # print(current_user.get_id())
        college = SESSION.query(User.name).filter(
            User.id == str(current_user.get_id())).first()[0]
        print(college)
        if college == '教务处':
            return super(NormalView, self).get_query()
        else:
            return super(NormalView, self).get_query().filter(
                Normal.课程归属学院 == college)


class DataView(ModelView):
    can_create = False
    can_delete = False
    column_display_pk = True
    column_list = ['序号', '课程归属学院', '任课教师', '课程号', '课程名称', '班级名称', '授课方式',
                   '线上教学方式', '线上教学慕课平台', '线上教学入口', '申报原因', '审核状态']
    column_sortable_list = ('授课方式', '序号', '课程归属学院', '课程号', '班级名称','审核状态')
    column_searchable_list = ('申报原因','课程归属学院', '任课教师', '课程号', '课程名称', '班级名称')
    column_default_sort = [('授课方式', False), ('序号', False)]

    # column_labels = {
    #     '转入线上授课日期': '课程异动开始时间',
    #     '结束线上授课日期': '课程异动结束时间',
    # }

    column_labels = dict(转入线上授课日期='课程异动开始时间', 结束线上授课日期='课程异动结束时间', 审核状态='备注',
                         线上教学慕课平台='线上教学平台')

    page_size = 50
    can_export = True
    export_types = ['xlsx']

    # form_extra_fields = {
    #     '线上教学方式': Select2TagsField()
    # }
    form_overrides = dict(
        # FIELD=MultipleSelect2Field,
        # 线上教学方式=MultipleSelect2Field,
        # 线上教学慕课平台=MultipleSelect2Field
    )

    CHOICES_TUPLE_1 = (
        ('自建慕课', '自建慕课'), ('平台提供的慕课', '平台提供的慕课'), ('直播', '直播'),
        ('录播（不建议使用）', '录播（不建议使用）'),
        ('无', '无'))
    CHOICES_TUPLE_2 = (
    ('雨课堂（建议）', '雨课堂（建议）'), ('超星学习通（建议）', '超星学习通（建议）'), ('腾讯会议', '腾讯会议'),
    ('爱课程(中国大学MOOC)', '爱课程(中国大学MOOC)'), ('智慧树', '智慧树'), ('钉钉直播', '钉钉直播'),
    ('学堂在线', '学堂在线'), ('其它', '其它'), ('无', '无'))

    form_choices = {
        '授课方式': [('转入线上教学', '转入线上教学'), ('延期授课', '延期授课'), ('线下教学', '线下教学')],
        # ('线下教学(仅限室外课程)', '线下教学(仅限室外课程)'),
        '线上教学方式': CHOICES_TUPLE_1,
        '线上教学慕课平台': CHOICES_TUPLE_2,
        #     '慕课平台': [('学校网络教学平台', '学校网络教学平台'), ('爱课程(中国大学MOOC)', '爱课程(中国大学MOOC)'),
        #              ('超星尔雅', '超星尔雅'), ('学堂在线', '学堂在线'), ('智慧树', '智慧树'), ('其它', '其它')]
    }

    form_args = dict(
        线上教学方式=dict(choices=CHOICES_TUPLE_1),
        线上教学慕课平台=dict(render_kw=dict(multiple="multiple"),
                      choices=CHOICES_TUPLE_2),
        # 转入线上授课时间 = dict(default_format='%M:%S', formats=('%H:%M:%S', '%M:%S'))
    )
    form_args = {
        '线上教学方式': {
            'render_kw': {
                "choices": [('自建慕课', '自建慕课'), ('平台提供的慕课', '平台提供的慕课'),
                            ('直播', '直播'), ('录播', '录播')],
            }
        },
        '慕课平台': {
            'render_kw': {"multiple": "multiple"},
        },
        '线上教学入口': {
            'render_kw': {

                'placeholder': '请填报平台网址、会议号（含密码）、群号等，「线上教学平台」选择"雨课堂"或"超星学习通"的老师无需填写线上教学入口'
            }
        },
        '申报原因': {
            'render_kw': {
                'placeholder': '请填写详细申报原因'
            }

        }
    }

    form_widget_args = {
        '课程归属学院': {'readonly': True},
        '任课教师': {'readonly': True},
        '课程号': {'readonly': True},
        '课程名称': {'readonly': True},
        '班级名称': {'readonly': True},
        # '转入线上授课时间' : {'data-role': u'timepickersecs',
        #                'data-date-format': u'mm:ss'},
    }

    def on_model_change(self, form, model, is_created):
        # form.线上教学方式.raw_data = str(form.线上教学方式.raw_data)
        if len(form.线上教学方式.raw_data) > 0:
            model.线上教学方式 = ','.join(form.线上教学方式.raw_data)

        # if len(form.线上教学慕课平台.raw_data) > 0:
        #     model.线上教学慕课平台 = ','.join(form.线上教学慕课平台.raw_data)
        # else:
        #     model.线上教学慕课平台 = ''
        pass

    def is_accessible(self):
        return current_user.is_authenticated

    # def on_form_prefill(self, form, id):
    #     form.线上教学方式.raw_data = '11'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))

    def get_query(self):
        print(current_user.get_id())
        college = SESSION.query(User.name).filter(
            User.id == str(current_user.get_id())).first()[0]
        if college == '教务处':
            return super(DataView, self).get_query()
        else:
            return super(DataView, self).get_query().filter(
                线上教学.课程归属学院 == college)


class OldDataView(ModelView):
    # can_create = False
    # can_delete = True
    # column_display_pk = True
    #
    # column_list = ['序号', '课程归属学院', '任课教师', '课程号', '课程名称',
    #                '班级名称', '授课方式',
    #                '线上教学方式', '线上教学慕课平台', '线上教学入口',
    #                '申报原因', '审核状态']
    # column_sortable_list = (
    # '授课方式', '序号', '课程归属学院', '课程号', '班级名称', '审核状态')
    # column_searchable_list = (
    # '申报原因', '课程归属学院', '任课教师', '课程号', '课程名称', '班级名称')
    # column_default_sort = [('授课方式', False), ('序号', False)]
    # # column_list = ['课程归属学院', '课程号', '课程名称', '班级号','班级名称', '教师工号','教师姓名', '周次', '星期', '节次', '教室', '教师姓名', '备注', '更新时间']
    # # column_sortable_list = ('课程归属学院', '课程名称', '班级名称', '教师姓名', '星期', '节次')
    # # column_searchable_list = ('课程归属学院', '课程名称', '班级名称', '教师姓名', '星期', '节次')
    #
    # # edit_modal = True
    #
    #
    # page_size = 50
    # can_export = True
    # export_types = ['xlsx']
    #
    # # form_extra_fields = {
    # #     '线上教学方式': Select2TagsField()
    # # }
    # form_overrides = dict(
    #     # FIELD=MultipleSelect2Field,
    #     # 线上教学方式=MultipleSelect2Field,
    #     # 线上教学慕课平台=MultipleSelect2Field
    # )
    #
    # form_widget_args = {
    #     '课程管理单位': {'readonly': True},
    #     '教工姓名': {'readonly': True},
    #     '课程号': {'readonly': True},
    #     '课程名称': {'readonly': True},
    #     '班级号': {'readonly': True},
    #     '班级名称': {'readonly': True},
    #     '教师工号': {'readonly': True},
    #     '教师姓名': {'readonly': True},
    # }

    can_create = False
    can_delete = False
    column_display_pk = True
    column_list = ['序号', '课程归属学院', '任课教师', '课程号', '课程名称', '班级名称', '授课方式',
                   '线上教学方式', '线上教学慕课平台', '线上教学入口', '申报原因', '审核状态']
    column_sortable_list = ('授课方式', '序号', '课程归属学院', '课程号', '班级名称','审核状态')
    column_searchable_list = ('申报原因','课程归属学院', '任课教师', '课程号', '课程名称', '班级名称')
    column_default_sort = [('授课方式', False), ('序号', False)]
    form_excluded_columns = [('最后更新时间')]

    # column_labels = {
    #     '转入线上授课日期': '课程异动开始时间',
    #     '结束线上授课日期': '课程异动结束时间',
    # }

    column_labels = dict(转入线上授课日期='课程异动开始时间', 结束线上授课日期='课程异动结束时间', 审核状态='备注',
                         线上教学慕课平台='线上教学平台')

    page_size = 50
    can_export = True
    export_types = ['xlsx']

    # form_extra_fields = {
    #     '线上教学方式': Select2TagsField()
    # }
    form_overrides = dict(
        # FIELD=MultipleSelect2Field,
        # 线上教学方式=MultipleSelect2Field,
        # 线上教学慕课平台=MultipleSelect2Field
    )

    CHOICES_TUPLE_1 = (
        ('自建慕课', '自建慕课'), ('平台提供的慕课', '平台提供的慕课'), ('直播', '直播'),
        ('录播（不建议使用）', '录播（不建议使用）'),
        ('无', '无'))
    CHOICES_TUPLE_2 = (
    ('雨课堂（建议）', '雨课堂（建议）'), ('超星学习通（建议）', '超星学习通（建议）'), ('腾讯会议', '腾讯会议'),
    ('爱课程(中国大学MOOC)', '爱课程(中国大学MOOC)'), ('智慧树', '智慧树'), ('钉钉直播', '钉钉直播'),
    ('学堂在线', '学堂在线'), ('其它', '其它'), ('无', '无'))

    form_choices = {
        '授课方式': [('转入线上教学', '转入线上教学'), ('延期授课', '延期授课'), ('线下教学', '线下教学')],
        # ('线下教学(仅限室外课程)', '线下教学(仅限室外课程)'),
        '线上教学方式': CHOICES_TUPLE_1,
        '线上教学慕课平台': CHOICES_TUPLE_2,
        #     '慕课平台': [('学校网络教学平台', '学校网络教学平台'), ('爱课程(中国大学MOOC)', '爱课程(中国大学MOOC)'),
        #              ('超星尔雅', '超星尔雅'), ('学堂在线', '学堂在线'), ('智慧树', '智慧树'), ('其它', '其它')]
    }

    form_args = dict(
        线上教学方式=dict(choices=CHOICES_TUPLE_1),
        线上教学慕课平台=dict(render_kw=dict(multiple="multiple"),
                      choices=CHOICES_TUPLE_2),
        # 转入线上授课时间 = dict(default_format='%M:%S', formats=('%H:%M:%S', '%M:%S'))
    )
    form_args = {
        '线上教学方式': {
            'render_kw': {
                "choices": [('自建慕课', '自建慕课'), ('平台提供的慕课', '平台提供的慕课'),
                            ('直播', '直播'), ('录播', '录播')],
            }
        },
        '慕课平台': {
            'render_kw': {"multiple": "multiple"},
        },
        '线上教学入口': {
            'render_kw': {

                'placeholder': '请填报平台网址、会议号（含密码）、群号等，「线上教学平台」选择"雨课堂"或"超星学习通"的老师无需填写线上教学入口'
            }
        },
        '申报原因': {
            'render_kw': {
                'placeholder': '请填写详细申报原因'
            }

        }
    }

    form_widget_args = {
        '课程归属学院': {'readonly': True},
        '任课教师': {'readonly': True},
        '课程号': {'readonly': True},
        '课程名称': {'readonly': True},
        '班级名称': {'readonly': True},
        '最后更新时间': {'readonly': True},
        # '转入线上授课时间' : {'data-role': u'timepickersecs',
        #                'data-date-format': u'mm:ss'},
    }

    def on_model_change(self, form, model, is_created):
        model.最后更新时间 = datetime.datetime.now()
        if len(form.线上教学方式.raw_data) > 0:
            model.线上教学方式 = ','.join(form.线上教学方式.raw_data)
        # if len(form.线上教学方式.raw_data) > 0:
        #     model.线上教学方式 = ','.join(form.线上教学方式.raw_data)

        # if len(form.线上教学慕课平台.raw_data) > 0:
        #     model.线上教学慕课平台 = ','.join(form.线上教学慕课平台.raw_data)
        # else:
        #     model.线上教学慕课平台 = ''
        pass

    def is_accessible(self):
        return current_user.is_authenticated

    # def on_form_prefill(self, form, id):
    #     form.线上教学方式.raw_data = '11'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))

    def get_query(self):
        print(current_user.get_id())
        college = SESSION.query(User.name).filter(
            User.id == str(current_user.get_id())).first()[0]
        if college == '教务处':
            return super(OldDataView, self).get_query()
        else:
            return super(OldDataView, self).get_query().filter(
                第六周课程.课程归属学院 == college)


class DelayDataView(ModelView):
    can_create = False
    can_delete = False
    column_display_pk = True
    column_list = ['序号', '课程归属学院', '任课教师', '课程号', '课程名称', '班级名称', '开课周次',
                   '授课方式', '申报原因', '是否已补课', '补课详情']
    column_sortable_list = (
    '序号', '课程归属学院', '课程号', '班级名称', '开课周次', '课程名称', '任课教师')
    column_searchable_list = ('课程号', '任课教师', '课程名称', '班级名称', '课程归属学院')
    column_default_sort = [('授课方式', False), ('序号', False)]

    column_labels = dict(授课方式='原因', 申报原因='备注', 是否已补课='是否已完成补课')

    page_size = 50
    can_export = True
    export_types = ['xlsx']

    form_overrides = dict(
        # FIELD=MultipleSelect2Field,
        # 线上教学方式=MultipleSelect2Field,
        # 线上教学慕课平台=MultipleSelect2Field
    )

    CHOICES_TUPLE_1 = (
        ('自建慕课', '自建慕课'), ('平台提供的慕课', '平台提供的慕课'), ('直播', '直播'), ('录播', '录播'),
        ('无', '无'))
    CHOICES_TUPLE_2 = (
        ('学校网络教学平台', '学校网络教学平台'), ('爱课程(中国大学MOOC)', '爱课程(中国大学MOOC)'),
        ('超星尔雅', '超星尔雅'), ('学堂在线', '学堂在线'), ('智慧树', '智慧树'), ('雨课堂', '雨课堂'),
        ('其它', '其它'), ('无', '无'))

    form_choices = {
        '是否已补课': [('是', '是'), ('否', '否')],
    }

    form_args = dict(
        # 线上教学方式=dict(render_kw=dict(multiple="multiple"),
        #             choices=CHOICES_TUPLE_1),
        # 线上教学慕课平台=dict(render_kw=dict(multiple="multiple"),
        #               choices=CHOICES_TUPLE_2),
    )
    form_args = {
        '是否已补课': {
            'render_kw': {
                "choices": [('是', '是'), ('否', '否')]
            },
        },
        '慕课平台': {
            'render_kw': {"multiple": "multiple"},
        },
        # '线上教学入口': {
        #     'render_kw': {
        #         'placeholder': '请填报线上教学网址、会议号（含密码）、群号等相关信息'
        #     }
        # },
        '补课详情': {
            'render_kw': {
                'placeholder': '请填写详细情况，应包含补课日期, 线上/线下教学方式等信息'
            }

        }
    }

    form_widget_args = {
        '课程归属学院': {'readonly': True},
        '任课教师': {'readonly': True},
        '课程号': {'readonly': True},
        '课程名称': {'readonly': True},
        '班级名称': {'readonly': True},
        '授课方式': {'readonly': True},
        # '申报原因': {'readonly': True},
        '开课周次': {'readonly': True},
        # '转入线上授课时间' : {'data-role': u'timepickersecs',
        #                'data-date-format': u'mm:ss'},
    }

    def on_model_change(self, form, model, is_created):
        # form.线上教学方式.raw_data = str(form.线上教学方式.raw_data)
        # if len(form.线上教学方式.raw_data) > 0:
        #     model.线上教学方式 = ','.join(form.线上教学方式.raw_data)

        # if len(form.线上教学慕课平台.raw_data) > 0:
        #     model.线上教学慕课平台 = ','.join(form.线上教学慕课平台.raw_data)
        # else:
        #     model.线上教学慕课平台 = ''
        pass

    def is_accessible(self):
        return current_user.is_authenticated

    # def on_form_prefill(self, form, id):
    #     form.线上教学方式.raw_data = '11'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))

    def get_query(self):
        print(current_user.get_id())
        college = SESSION.query(User.name).filter(
            User.id == str(current_user.get_id())).first()[0]
        if college == '教务处':
            return super(DelayDataView, self).get_query()
        else:
            return super(DelayDataView, self).get_query().filter(
                延期课程.课程归属学院 == college)


# admin.add_view(
#     DataView(线上教学, SESSION(), '报备', endpoint='admin_view_normal'))

# admin.add_view(OldDataView(特殊课程安排, SESSION(),'特殊课程填报', endpoint='admin_view_pre'))

# admin.add_view(OldDataView(第六周课程, SESSION(),'报备', endpoint='admin_view_normal'))

# admin.add_view(Week6DataView(第六周课程, SESSION(),'第六周历史数据(谨慎填写)'))
# admin.add_view(NormalView(Normal, SESSION()))
# admin.add_view(
#     DelayDataView(延期课程, SESSION(), '延期课程补报', endpoint='admin_view_delay'))


admin.add_view(TeacherView(在职教师, SESSION()))
admin.add_view(TmpTeacherView(外聘教师, SESSION()))


# admin.add_view(ArrangeView(开课安排, SESSION()))


# migrate = Migrate(app, db)


def make_shell_context():
    pass


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='localhost', port=8080,
                                        use_debugger=True))


@manager.command
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbossity=2).run(tests)


if __name__ == '__main__':
    manager.run()
