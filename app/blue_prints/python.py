# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g
from app import app
from ..models import *

python_bp = Blueprint('python_bp', __name__, url_prefix='/python')
series_name = 'Python 教程'


def get_sub_dict(sub_comment_all, comment):
    len_sub_comment_all = len(sub_comment_all)

    all_sub_list = []
    for i in list(range(len_sub_comment_all)):
        sub_c_list = sub_comment_all[i]
        user_sub_c_list = []
        for sub_c in sub_c_list:
            user = User.query.filter_by(id=sub_c.user_id).first()

            user_sub_c = (user, sub_c)
            user_sub_c_list.append(user_sub_c)
        all_sub_list.append(user_sub_c_list)

    com_to_sub_dict, _num = {}, 0
    # com_to_sub_dict = {parent_comment_1: [(sub_user1, sub_comment1), (sub_user2, sub_comment2)], parent_comment_2: []}
    for com in comment:
        com_to_sub_dict[com.id] = all_sub_list[_num]
        _num += 1
    return com_to_sub_dict


@python_bp.route('/')
@python_bp.route('/1ch')
def intro():
    a_id = 1
    chap_num = 1
    article = Article.query.filter_by(id=a_id).first()
    comment = Comment.query.filter_by(article_id=article.id).all()
    if not comment:
        user_comment = None
        com_to_sub_dict = None
    else:
        sub_comment_all = [SubComment.query.filter_by(main_comment_id=com.id).all() for com in comment]
        # sub_comment_all is like [[<SubComment from parent_comment1, content=None.], []]

        com_to_sub_dict = get_sub_dict(sub_comment_all, comment)

        user = [User.query.filter_by(id=com.user_id).first() for com in comment]
        user_comment = zip(user, comment)
    return render_template('python/python_1ch.html',
                           chap_num=chap_num+1,
                           article=article,
                           user_comment=user_comment,
                           com_to_sub_dict=com_to_sub_dict
                           )


@python_bp.route('/2ch')
def sec_chapter():
    a_id = 2
    chap_num = 2
    article = Article.query.filter_by(id=a_id).first()
    comment = Comment.query.filter_by(article_id=article.id).all()
    if not comment:
        user_comment = None
        com_to_sub_dict = None
    else:
        sub_comment_all = [SubComment.query.filter_by(main_comment_id=com.id).all() for com in comment]
        # sub_comment_all is like [[<SubComment from parent_comment1, content=None.], []]

        com_to_sub_dict = get_sub_dict(sub_comment_all, comment)

        user = [User.query.filter_by(id=com.user_id).first() for com in comment]
        user_comment = zip(user, comment)

    return render_template('python/python_2ch.html',
                           chap_num=chap_num+1,
                           article=article,
                           user_comment=user_comment,
                           com_to_sub_dict=com_to_sub_dict
                           )


@python_bp.route('/3ch')
def thi_chapter():
    a_id = 3
    chap_num = 3
    article = Article.query.filter_by(id=a_id).first()
    comment = Comment.query.filter_by(article_id=article.id).all()
    if not comment:
        user_comment = None
        com_to_sub_dict = None
    else:
        sub_comment_all = [SubComment.query.filter_by(main_comment_id=com.id).all() for com in comment]
        # sub_comment_all is like [[<SubComment from parent_comment1, content=None.], []]

        com_to_sub_dict = get_sub_dict(sub_comment_all, comment)

        user = [User.query.filter_by(id=com.user_id).first() for com in comment]
        user_comment = zip(user, comment)

    return render_template('python/python_3ch.html',
                           chap_num=chap_num+1,
                           article=article,
                           user_comment=user_comment,
                           com_to_sub_dict=com_to_sub_dict
                           )


@python_bp.route('/4ch')
def four_chapter():
    a_id = 4
    chap_num = 4
    article = Article.query.filter_by(id=a_id).first()
    comment = Comment.query.filter_by(article_id=article.id).all()
    if not comment:
        user_comment = None
        com_to_sub_dict = None
    else:
        sub_comment_all = [SubComment.query.filter_by(main_comment_id=com.id).all() for com in comment]
        # sub_comment_all is like [[<SubComment from parent_comment1, content=None.], []]

        com_to_sub_dict = get_sub_dict(sub_comment_all, comment)

        user = [User.query.filter_by(id=com.user_id).first() for com in comment]
        user_comment = zip(user, comment)

    return render_template('python/python_4ch.html',
                           chap_num=chap_num+1,
                           article=article,
                           user_comment=user_comment,
                           com_to_sub_dict=com_to_sub_dict
                           )


@python_bp.route('/5ch')
def fifth_chapter():
    a_id = 5
    chap_num = 5
    article = Article.query.filter_by(id=a_id).first()
    comment = Comment.query.filter_by(article_id=article.id).all()
    if not comment:
        user_comment = None
        com_to_sub_dict = None
    else:
        sub_comment_all = [SubComment.query.filter_by(main_comment_id=com.id).all() for com in comment]
        # sub_comment_all is like [[<SubComment from parent_comment1, content=None.], []]

        com_to_sub_dict = get_sub_dict(sub_comment_all, comment)

        user = [User.query.filter_by(id=com.user_id).first() for com in comment]
        user_comment = zip(user, comment)

    return render_template('python/python_5ch.html',
                           chap_num=chap_num+1,
                           article=article,
                           user_comment=user_comment,
                           com_to_sub_dict=com_to_sub_dict
                           )

app.register_blueprint(python_bp)
