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
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user
from flask_marshmallow import Marshmallow
from flask_migrate import MigrateCommand
from flask_script import Manager, Server
from flask_script import Shell
from werkzeug.utils import redirect

from app.create_app import create_app
from app.models import Coronavirus, User
from app.views import main_blueprint

app, SESSION = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
ma = Marshmallow(app)
admin = Admin(app, name='开课统计', template_mode='bootstrap3')
login = LoginManager(app)

app.register_blueprint(main_blueprint)


@login.user_loader
def load_user(u_id):
    return SESSION().query(User).filter(User.id == u_id).first()


class DataView(ModelView):
    can_create = False
    can_delete = False
    column_display_pk = True
    column_sortable_list = ('序号', '课程归属学院', '课程号', '班级名称')
    column_searchable_list = ('课程归属学院', '课程号', '任课教师', '课程名称', '班级名称')
    column_default_sort = '序号'
    page_size = 50
    can_export = True
    export_types = ['csv', 'xlsx']

    form_widget_args = {
        '课程归属学院': {'readonly':True},
        '任课教师': {'readonly':True},
        '课程号': {'readonly':True},
        '课程名称': {'readonly':True},
        '班级名称': {'readonly':True}
    }

    form_choices = {
        '线上教学方式': [('直播', '直播'), ('录播', '录播')],
        '慕课平台': [('0', '超星'), ('1', '其它')],
        '是否延期': [('0', '是'), ('1', '否')],
    }

    # list_columns = ['序号', '班级名称']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))

    def get_query(self):
        print (current_user.get_id())
        college = SESSION.query(User.name).filter(User.id == str(current_user.get_id())).first()[0]
        if college == '教务处':
            return super(DataView, self).get_query()
        else:
            return super(DataView, self).get_query().filter(Coronavirus.课程归属学院 == college)


admin.add_view(DataView(Coronavirus, SESSION()))


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
