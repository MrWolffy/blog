# -*- coding: utf-8 -*-

import os

SECRET_KEY = 'LJpython3.5_web'
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:lijian_python_2017@localhost:3306/blog?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 40

UPLOAD_FOLDER = os.getcwd() + '/app/static/images'

ADMIN_EMAIL = 'lijianpku15@163.com'




