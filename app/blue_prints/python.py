# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g
from .global_fun import *

python_bp = Blueprint('python_bp', __name__, url_prefix='/python')
series_name = 'Python 教程'


@python_bp.route('/')
@python_bp.route('/1ch')
def intro():
    a_id = 1
    chap_num = 1
    article, user_comment, com_to_sub_dict = get_data(a_id)
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
    article, user_comment, com_to_sub_dict = get_data(a_id)
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
    article, user_comment, com_to_sub_dict = get_data(a_id)
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
    article, user_comment, com_to_sub_dict = get_data(a_id)
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
    article, user_comment, com_to_sub_dict = get_data(a_id)
    return render_template('python/python_5ch.html',
                           chap_num=chap_num+1,
                           article=article,
                           user_comment=user_comment,
                           com_to_sub_dict=com_to_sub_dict
                           )

app.register_blueprint(python_bp)
