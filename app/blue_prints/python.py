# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g
from app import app
from ..models import *

python_bp = Blueprint('python_bp', __name__, url_prefix='/python')


@python_bp.route('/')
@python_bp.route('/1st')
def intro():
    a_id = 1
    article = Article.query.filter_by(id=a_id).first()
    comment = Comment.query.filter_by(article_id=article.id).all()
    return render_template('python_intro.html',
                           article=article,
                           comment=comment)


@python_bp.route('/2nd')
def sec_chapter():
    a_id = 2
    article = Article.query.filter_by(id=a_id).first()
    comment = Comment.query.filter_by(article_id=article.id).all()
    return render_template('python_2.html',
                           article=article,
                           comment=comment)

app.register_blueprint(python_bp)
