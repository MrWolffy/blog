# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import db, app

# 版本迁移的bug太TM藏得深了，de了我一整天！！！

migrate = Migrate(app, db)  # 初始化迁移类，登记需要迁移的数据库
manager = Manager(app)  # 创建管理者对象
manager.add_command('db', MigrateCommand)  # 为管理者添加迁移命令

if __name__ == '__main__':
    manager.run()
