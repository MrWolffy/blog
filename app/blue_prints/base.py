# -*- coding: utf-8 -*-

from config import ADMIN_EMAIL
from flask import Blueprint, render_template, request, g, session, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from ..models import *
import json
from ..forms import UserRegisterForm, LoginForm, SuggestionForm, EditForm
from functools import reduce
from datetime import datetime

# 创建蓝图
base_bp = Blueprint('base_bp', __name__, url_prefix='')


# 加载已登录的用户
@lm.user_loader
def load_user(id):
    if User.query.get(int(id)):
        print('load user: {}'.format(int(id)))
        return User.query.get(int(id))


# 主页视图
@base_bp.route('/')
@base_bp.route('/home')
def home():
    form = SuggestionForm()
    alert_status, info, status = 'none', '', 'danger'
    return render_template('home.html',
                           form=form,
                           alert_status=alert_status,
                           status=status,
                           info=info)


# 主页接受建议信息 视图
@base_bp.route('/suggestion', methods=['GET', 'POST'])
def suggestion():
    form = SuggestionForm()
    alert_status, info, status = 'none', '', 'danger'
    if form.validate_on_submit():
        status = 'success'
        info = '恭喜你，提交成功，感谢你的建议！'
        sug = Suggestion()
        sug.username = form.username.data
        sug.email = form.email.data
        sug.title = form.title.data
        sug.content = form.content.data
        db.session.add(sug)
        db.session.commit()
    else:
        alert_status = 'block'
        info = '提交失败，请完整填写表单'
    return render_template('home.html',
                           form=form,
                           alert_status=alert_status,
                           status=status,
                           info=info)


# 注册视图
@base_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegisterForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        g.user = user
        # 给注册的用户分配角色（权限）
        user.role = []
        if user.email != ADMIN_EMAIL:
            user.role.append(Role.query.filter_by(id=1).first())
            user.role.append(Role.query.filter_by(id=2).first())
        else:
            user.role.append(Role.query.filter_by(id=4).first())
        db.session.add(user)
        db.session.commit()
        session.username = user.username
        return redirect(url_for('base_bp.login'))
    return render_template('register.html', form=form)


# 使用ajax验证注册部分
@base_bp.route('/validate_username', methods=['GET', 'POST'])
def validate_username():
    username = request.form['username']
    print(username)
    if User.query.filter_by(username=username).first():  # 用户名被占用
        return json.dumps({'issue': 'username', 'OK': False})  # 返回失败
    if not User.query.filter_by(username=username).first():  # 用户名未被占用
        return json.dumps({'issue': 'username', 'OK': True})  # 返回成功（下同）


@base_bp.route('/validate_email', methods=['GET', 'POST'])
def validate_email():
    email = request.form['email']
    print(email)
    if User.query.filter_by(email=email).first():
        return json.dumps({'issue': 'email', 'OK': False})
    if not User.query.filter_by(email=email).first():
        return json.dumps({'issue': 'email', 'OK': True})


# 登录视图
@base_bp.route('/login', methods=['GET', 'POST'])
def login():
    permission_code, error, alert_status = 0, '', 'none'
    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        g.user = User.query.filter_by(email=email).first()
        if g.user and g.user.verify_password(password):
            permission_code = reduce(lambda x, y: x.permission | y.permission, g.user.role)
            if permission_code >= 1:  # 判断条件，附加一个权限检查
                login_user(g.user)
                return redirect(url_for('base_bp.home'))
        else:
            error = '账号或密码错误，无法登录！'
            alert_status = 'block'
    # 向前端传出一个permission_code，方便前端页面上验证权限
    return render_template('login.html',
                           form=form,
                           permission_code=permission_code,
                           error=error,
                           alert_status=alert_status)


@login_required
@base_bp.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    change = 0
    # 在前段的modal页面修改个人资料部分，因为可以单独修改某一字段，所以用request自带的方法，不用form
    if request.method == "POST":
        if request.form.get('username'):
            current_user.user = request.form.get('username')
            change += 1
        if request.form.get('password'):
            current_user.password = request.form.get('password')
            change += 1
        if request.form.get('sign'):
            current_user.sign = request.form.get('sign')
            change += 1
        if change > 0:
            db.session.add(current_user)
            db.session.commit()
            return render_template('user_profile.html')
    return render_template('user_profile.html')


@base_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base_bp.home'))


# ajax 提交评论
@base_bp.route('/comment_get/<article_id>', methods=['GET', 'POST'])
def comment_get(article_id):
    article = Article.query.filter_by(id=article_id).first()
    user = current_user
    info = '提交失败，请稍后再试。'
    status = 'warning'
    if request.method == "POST":
        comment = Comment()
        comment.title = request.form.get('title')
        comment.content = request.form.get('content')
        comment.article_id = article.id
        comment.user_id = user.id
        comment.speaker = user.username
        comment.speaker_avatar = user.avatar
        comment.posted = datetime.utcnow()
        db.session.add(comment)
        db.session.commit()
        info = "提交成功！"
        status = 'success'
        flash(status, info)
        return redirect(article.url)
    flash(status, info)
    return redirect(article.url)


app.register_blueprint(base_bp)
