# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g
from app import app
from ..models import *

python_bp = Blueprint('python_bp', __name__, url_prefix='/python')
series_name = 'Python 教程'


@python_bp.route('/')
@python_bp.route('/1ch')
def intro():
    a_id = 1
    article = Article.query.filter_by(id=a_id).first()
    comment = Comment.query.filter_by(article_id=article.id).all()
    user = [User.query.filter_by(id=com.user_id).first() for com in comment]
    user_comment = zip(user, comment)
    return render_template('python/python_1ch.html',
                           article=article,
                           user_comment=user_comment, )


@python_bp.route('/2ch')
def sec_chapter():
    a_id = 2
    article = Article.query.filter_by(id=a_id).first()
    comment = Comment.query.filter_by(article_id=article.id).all()
    user = [User.query.filter_by(id=com.user_id).first() for com in comment]
    user_comment = zip(user, comment)
    return render_template('python/python_1ch.html',
                           article=article,
                           user_comment=user_comment)

app.register_blueprint(python_bp)
