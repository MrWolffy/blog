# -*- coding: utf-8 -*-

from config import ADMIN_EMAIL, UPLOAD_FOLDER
from flask import Blueprint, render_template, request, g, session, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from app import app, db, lm, mail
from ..models import *
import json
import os
import re
from threading import Thread
from ..forms import UserRegisterForm, LoginForm, SuggestionForm, EditForm
from functools import reduce
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# 创建蓝图
base_bp = Blueprint('base_bp', __name__, url_prefix='')


# 异步发送邮件方法
def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject,
                    recipients=[to])
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # 在新线程中发送邮件
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


# 安全验证相关
def generate_confirmation_token(user_id, email, expired=600):
    s = Serializer(current_app.config['SECRET_KEY'], expired)
    return s.dumps({'id': user_id, 'email': email})


# 用id和email是否配对来检查, 返回[验证通过与否，验证的用户id]
def confirm(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        user_id = data.get('id')
        email = data.get('email')
    except :
        return [False, None]
    if user_id != User.query.filter_by(email=email).first().id:
        return [False, None]
    return [True, user_id]


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

        # 异步发送欢迎邮件
        send_email(user.email, '欢迎注册eztutor', 'email/welcome_mail', user=user)

        return redirect(url_for('base_bp.login'))
    return render_template('user/register.html', form=form)


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
    return render_template('user/login.html',
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
            flash('更改成功！')  # 在前端用js添加提示
            return render_template('user/user_profile.html')
    return render_template('user/user_profile.html')


# 修改头像
@login_required
@base_bp.route('/avatar_change', methods=['GET', 'POST'])
def avatar_change():
    avatar = request.files['change-avatar']
    if avatar:
        f_name = avatar.filename
        ALLOWED_EXTENTIONS = ['png', 'jpg', 'jpeg', 'gif']
        flag = '.' in f_name and f_name.rsplit('.', 1)[1] in ALLOWED_EXTENTIONS
        if not flag:
            flash('文件类型错误。')
            return redirect('user/{}'.format(current_user.username))
        avatar.save('{}/{}_{}'.format(UPLOAD_FOLDER, current_user.username, f_name))
        if current_user.avatar != '../static/images/avatar/default.png':
            os.remove(os.getcwd() + '/app{}'.format(current_user.avatar))
        current_user.avatar = '/static/images/avatar/{}_{}'.format(current_user.username, f_name)
        db.session.add(current_user)
        db.session.commit()
    return redirect('user/{}'.format(current_user.username))


# 忘记密码
@base_bp.route('/user/forget_password', methods=['GET', 'POST'])
def forget_password():
    return render_template('user/forget_password.html')


# 修改密码，在此处发邮件到邮箱，ajax处理请求
@base_bp.route('/user/password_change', methods=['GET', 'POST'])
def password_change():
    email = request.form['email']
    user = User.query.filter_by(email=email).first()
    token = generate_confirmation_token(user.id, email)
    send_email(user.email, 'eztutor账号安全提醒', 'email/warning', user=user, token=token)
    issue = '一封确认密码修改的邮件已经发送到您的注册邮箱！'
    return json.dumps({'msg': issue, 'status': 'block'})


# 修改密码,在此处修改、提交、验证，往数据库提交数据
@base_bp.route('/password_change_validate/<token>', methods=['GET', 'POST'])
def password_change_validate(token):
    if confirm(token)[0]:
        if request.method == "POST":
            user = User.query.filter_by(id=confirm(token)[1]).first()
            if request.form.get('password'):
                user.password = request.form.get('password')
            db.session.add(user)
            db.session.commit()
            flash('密码修改成功！')
            return redirect(url_for('base_bp.login'))

        return render_template('user/change_password.html', token=token)
    else:
        return 404


@base_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base_bp.home'))


# 提交评论
@base_bp.route('/comment_get/<article_id>', methods=['GET', 'POST'])
def comment_get(article_id):
    article = Article.query.filter_by(id=article_id).first()
    user = current_user
    info = '提交失败，请稍后再试。'
    status = 'warning'
    if request.method == "POST":
        comment = Comment()
        comment.title = request.form.get('title')
        ori_content = request.form.get('content')
        comment.content = re.sub(r'<script>*</script>', '', ori_content)
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


# 提交子评论
@base_bp.route('/sub_comment_get', methods=['GET', 'POST'])
def sub_comment_get():
    user = current_user
    info = '非常抱歉，回复失败，请稍后重试。'
    status = 'warning'
    if request.method == "POST":
        sub_comment = SubComment()
        # 后端传过来的是bytes，需要用decode先转为str
        data = json.loads(request.get_data().decode('utf-8'))

        sub_comment.main_comment_id = int(data['main_comment_id'])
        ori_content = data['content']
        sub_comment.content = re.sub(r'<script>*</script>', '', ori_content)
        sub_comment.user_id = user.id
        sub_comment.posted = datetime.utcnow()

        db.session.add(sub_comment)
        db.session.commit()
        info = "感谢您的参与，回复成功！"
        status = 'success'
        return json.dumps({'info': info, 'status': status})
    else:
        return json.dumps({'info': info, 'status': status})


app.register_blueprint(base_bp)
