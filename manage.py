#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: sadscv
@time: 2019/09/26 21:18
@file: manage.py

@desc: 
"""
import os

from flask import url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2TagsField
from flask_babelex import Babel
from flask_login import LoginManager, current_user
from flask_marshmallow import Marshmallow
from flask_migrate import MigrateCommand
from flask_script import Manager, Server
from flask_script import Shell
from werkzeug.utils import redirect

from app.create_app import create_app
from app.gen_models import 开课安排
from app.models import Coronavirus, User, MultipleSelect2Field, Normal
from app.views import main_blueprint

app, SESSION = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
ma = Marshmallow(app)
admin = Admin(app,
              name='开课统计',
              template_mode='bootstrap3',
              index_view=AdminIndexView(
                  template='welcome.html',
                  url='/admin')
              )
login = LoginManager(app)
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'

app.register_blueprint(main_blueprint)


@login.user_loader
def load_user(u_id):
    return SESSION().query(User).filter(User.id == u_id).first()


class ArrangeView(ModelView):
    form_widget_args = {
        '课程归属学院': {'readonly': True},
        '任课教师': {'readonly': True},
        '课程号': {'readonly': True},
        '课程名称': {'readonly': True},
        '班级名称': {'readonly': True}
    }


class NormalView(ModelView):
    can_create = False
    can_delete = False
    column_display_pk = True
    column_list = ['序号', '课程归属学院', '任课教师', '课程号', '课程名称', '班级号', '班级名称', '线上开课',
                   '增补时段', '其它备注']
    # column_list = ['序号', '课程归属学院', '任课教师', '课程号', '课程名称', '班级号', '班级名称', '线上开课',
    #                '是否转入线下', '增补时段', '其它备注']
    column_sortable_list = ('序号', '课程归属学院', '任课教师', '课程名称', '课程号', '班级名称', '线上开课')
    column_searchable_list = ('课程号', '任课教师', '课程名称', '班级名称', '课程归属学院', '序号', '线上开课')
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
        增补时段=MultipleSelect2Field,
    )
    choices_tuple_add = (
        ('周一-12', '周一-12'), ('周一-3', '周一-3'), ('周一-4', '周一-4'), ('周一-5', '周一-5'), ('周一-67', '周一-67'), ('周一-89', '周一-89'), ('周一-晚', '周一-晚'),
        ('周二-12', '周二-12'), ('周二-3', '周二-3'), ('周二-4', '周二-4'), ('周二-5', '周二-5'), ('周二-67', '周二-67'), ('周二-89', '周二-89'), ('周二-晚', '周二-晚'),
        ('周三-12', '周三-12'), ('周三-3', '周三-3'), ('周三-4', '周三-4'), ('周三-5', '周三-5'), ('周三-67', '周三-67'), ('周三-89', '周三-89'), ('周三-晚', '周三-晚'),
        ('周四-12', '周四-12'), ('周四-3', '周四-3'), ('周四-4', '周四-4'), ('周四-5', '周四-5'), ('周四-67', '周四-67'), ('周四-89', '周四-89'), ('周四-晚', '周四-晚'),
        ('周五-12', '周五-12'), ('周五-3', '周五-3'), ('周五-4', '周五-4'), ('周五-5', '周五-5'), ('周五-67', '周五-67'), ('周五-89', '周五-89'), ('周五-晚', '周五-晚'),
        ('周六-12', '周六-12'), ('周六-3', '周六-3'), ('周六-4', '周六-4'), ('周六-5', '周六-5'), ('周六-67', '周六-67'), ('周六-89', '周六-89'), ('周六-晚', '周六-晚'),
        ('周日-12', '周日-12'), ('周日-3', '周日-3'), ('周日-4', '周日-4'), ('周日-5', '周日-5'), ('周日-67', '周日-67'), ('周日-89', '周日-89'), ('周日-晚', '周日-晚')
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
            model.增补时段= ''

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
    column_list = ['序号', '课程归属学院', '任课教师', '课程号', '课程名称', '班级名称', '是否延期',
                   '线上教学方式', '慕课平台', '直播或录播软件_选填']
    column_sortable_list = ('序号', '课程归属学院', '课程号', '班级名称', '是否延期')
    column_searchable_list = ('课程号', '任课教师', '课程名称', '班级名称', '课程归属学院', '序号')
    column_default_sort = '序号'
    page_size = 50
    can_export = True
    export_types = ['xlsx']

    # form_extra_fields = {
    #     '线上教学方式': Select2TagsField()
    # }
    form_overrides = dict(
        # FIELD=MultipleSelect2Field,
        线上教学方式=MultipleSelect2Field,
        慕课平台=MultipleSelect2Field
    )

    # form_choices = {
    #     '线上教学方式': [('自建慕课', '自建慕课'), ('平台提供的慕课', '平台提供的慕课'), ('直播', '直播'), ('录播', '录播')],
    #     '慕课平台': [('学校网络教学平台', '学校网络教学平台'), ('爱课程(中国大学MOOC)', '爱课程(中国大学MOOC)'),
    #              ('超星尔雅', '超星尔雅'), ('学堂在线', '学堂在线'), ('智慧树', '智慧树'), ('其它', '其它')]
    # }
    CHOICES_TUPLE_1 = (
        ('自建慕课', '自建慕课'), ('平台提供的慕课', '平台提供的慕课'), ('直播', '直播'), ('录播', '录播'))
    CHOICES_TUPLE_2 = (
        ('学校网络教学平台', '学校网络教学平台'), ('爱课程(中国大学MOOC)', '爱课程(中国大学MOOC)'),
        ('超星尔雅', '超星尔雅'), ('学堂在线', '学堂在线'), ('智慧树', '智慧树'), ('其它', '其它'))
    form_args = dict(
        线上教学方式=dict(render_kw=dict(multiple="multiple"),
                    choices=CHOICES_TUPLE_1),
        慕课平台=dict(render_kw=dict(multiple="multiple"), choices=CHOICES_TUPLE_2)
    )
    # form_args = {
    #     '线上教学方式': {
    #         'render_kw': {"multiple": "multiple",
    #                       "choices": [('自建慕课', '自建慕课'), ('平台提供的慕课', '平台提供的慕课'), ('直播', '直播'), ('录播', '录播')]}
    #     },
    #     # '慕课平台': {
    #     #     'render_kw': {"multiple": "multiple"},
    #     # }
    # }

    form_widget_args = {
        '课程归属学院': {'readonly': True},
        '任课教师': {'readonly': True},
        '课程号': {'readonly': True},
        '课程名称': {'readonly': True},
        '班级名称': {'readonly': True}
    }

    def on_model_change(self, form, model, is_created):
        # form.线上教学方式.raw_data = str(form.线上教学方式.raw_data)
        if len(form.线上教学方式.raw_data) > 0:
            model.线上教学方式 = ','.join(form.线上教学方式.raw_data)

        if len(form.慕课平台.raw_data) > 0:
            model.慕课平台 = ','.join(form.慕课平台.raw_data)
        else:
            model.慕课平台 = ''

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
                Coronavirus.课程归属学院 == college)


# admin.add_view(DataView(Coronavirus, SESSION()))
admin.add_view(NormalView(Normal, SESSION()))


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
