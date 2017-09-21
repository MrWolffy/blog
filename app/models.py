# -*- coding: utf-8 -*-

from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Permission:
    LOGIN = 0x01
    COMMENT = 0x02
    WRITE = 0x04
    ALL = 0xff
'''
用户权限：
受限用户 == 1，仅能登录
一般用户 == 3，能登录和评论
高级用户 == 7，能登录、评论、发表教程
管理员用户 == 255，所有权限
'''


user_role_table = db.Table(
    'user_role_db', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    permission = db.Column(db.Integer)
    default = db.Column(db.Boolean, default=False, index=True)
    user = db.relationship('User', secondary=user_role_table, backref=db.backref('role_per', lazy='dynamic'))

    def __repr__(self):
        return '<Role %s>' % self.name


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    sign = db.Column(db.String(255), index=True, default='这个人比较懒，什么都没有留下。')
    password_hash = db.Column(db.String(220), index=True)
    role = db.relationship('Role', secondary=user_role_table, backref=db.backref('user_role', lazy='dynamic'))
    comment = db.relationship('Comment', backref=db.backref('provider'))
    sub_comment = db.relationship('SubComment', backref=db.backref('sub_com_provider'))
    # interested = db.relationship('Article', backref=db.backref('interested_user'))
    wrote = db.relationship('Article', backref=db.backref('author'))
    last_seen = db.Column(db.DateTime, index=True)
    avatar = db.Column(db.String(128), default='/static/images/avatar/default.png')

    def __repr__(self):
        return '<User %s>' % self.username

    # 几个 is_### 属性是flask.login要求的，必须附上
    @property
    def is_authenticated(self):  # 是否已经登陆
        return True

    @property
    def is_active(self):  # 是否有登陆权限
        return True

    @property
    def is_anonymous(self):  # 是否允许匿名访问
        return False

    @property
    def password(self):
        raise AttributeError('Password is not visible!')

    @password.setter  # 关于password的设置方法
    def password(self, password):  # 将password hash
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):  # 验证password 哈希之后是否与之前存储的 password_hash相等
        return check_password_hash(self.password_hash, password)

    def can(self, permission):
        return self.role is not None and (self.role.permission & permission) == permission

    def is_administrator(self):
        return self.can(Permission.ALL)

    def get_id(self):
        try:
            return self.id
        except NameError:
            return 'Failed to get id.'


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(20), index=True)
    comment = db.relationship('Comment', backref='topic')
    url = db.Column(db.String(128), index=True)
    time = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return '<Article {}>'.format(self.name)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sub_comment = db.relationship('SubComment', backref='parent_comment')
    title = db.Column(db.String(255), index=True)
    content = db.Column(db.Text)
    speaker = db.Column(db.String(30), index=True)
    speaker_avatar = db.Column(db.String(128))
    posted = db.Column(db.DateTime)

    def __repr__(self):
        return '<Comment {}>'.format(self.content)


class SubComment(db.Model):
    __tablename__ = "subcomment"
    id = db.Column(db.Integer, primary_key=True)
    main_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    posted = db.Column(db.DateTime)

    def __repr__(self):
        return '<SubComment from parent_comment{}, content={}.'.format(self.main_comment_id, self.content)


class Suggestion(db.Model):
    __tablename__ = 'suggestion'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(128), index=True)
    title = db.Column(db.String(220), index=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Suggestion "{}" from {}'.format(self.title, self.username)

