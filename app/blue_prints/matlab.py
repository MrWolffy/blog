# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g
from app import app
from ..models import *

matlab_bp = Blueprint('python_bp', __name__, url_prefix='/matlab')


@matlab_bp.route('/')
@matlab_bp.route('/1ch')
def intro():
    a_id = 1
    article = Article.query.filter_by(id=a_id).first()
    comment = Comment.query.filter_by(article_id=article.id).all()
    user = [User.query.filter_by(id=com.user_id).first() for com in comment]
    user_comment = zip(user, comment)
    return render_template('MATLAB_ch1.html',
                           article=article,
                           user_comment=user_comment)

app.register_blueprint(matlab_bp)
