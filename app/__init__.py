# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from app.blue_prints.admin import admin_bp
# from app.blue_prints.base import base_bp
# from app.blue_prints.python import python_bp
# import flask_whooshalchemyplus

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

lm = LoginManager()
lm.session_protection = 'basic'
lm.login_view = 'login'
lm.init_app(app)


from app.blue_prints import admin, base, python


