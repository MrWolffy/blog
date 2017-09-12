# -*- coding: utf-8 -*-

from app import app, db, lm
from app.models import User, Role, Article, Comment
from functools import reduce

test_email = '821972394@qq.com'
test_username = "amuro"
test_password = '123456'
test_company_name = 'eztutor'
test_user = User.query.filter_by(email=test_email).first()
print(type(test_user.role))
print(test_user.role)
for i in test_user.role:
    print(i.permission)
    print(i.name)
print(reduce(lambda x, y: x.permission | y.permission, test_user.role))
print(1 | 2)
print(reduce(lambda x, y: x | y, [1]))
