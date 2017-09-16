# -*- coding: utf-8 -*-


from flask import render_template, Flask
from functools import reduce

app = Flask(__name__)

app.config.from_object('config')

msg = render_template('welcome_mail.html')
print(msg)
print(type(msg))
