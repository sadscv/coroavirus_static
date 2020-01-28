#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: sadscv
@time: 2019/09/26 21:18
@file: manage.py

@desc: 
"""
import os

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_marshmallow import Marshmallow
from flask_migrate import MigrateCommand
from flask_script import Manager, Server
from flask_script import Shell

from app.create_app import create_app
from app.models import 专业
from app.views import main_blueprint

app, SESSION = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
ma = Marshmallow(app)
admin = Admin(app, name='microblog', template_mode='bootstrap3')
app.register_blueprint(main_blueprint)
mv = ModelView(专业, SESSION())
mv.column_default_sort = '专业号'
admin.add_view(mv)


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
