# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g
from .global_fun import *

matlab_bp = Blueprint('matlab_bp', __name__, url_prefix='/matlab')


@matlab_bp.route('/')
@matlab_bp.route('/1ch')
def intro():
    a_id = 6
    chap_num = 1
    article, user_comment, com_to_sub_dict = get_data(a_id)
    return render_template('matlab/MATLAB_ch1.html',
                           chap_num=chap_num + 1,
                           article=article,
                           user_comment=user_comment,
                           com_to_sub_dict=com_to_sub_dict
                           )


@matlab_bp.route('/2ch')
def sec_chapter():
    a_id = 7
    chap_num = 2
    article, user_comment, com_to_sub_dict = get_data(a_id)
    return render_template('matlab/MATLAB_ch2.html',
                           chap_num=chap_num + 1,
                           article=article,
                           user_comment=user_comment,
                           com_to_sub_dict=com_to_sub_dict
                           )


@matlab_bp.route('/3ch')
def thi_chapter():
    a_id = 8
    chap_num = 3
    article, user_comment, com_to_sub_dict = get_data(a_id)
    return render_template('matlab/MATLAB_ch3.html',
                           chap_num=chap_num + 1,
                           article=article,
                           user_comment=user_comment,
                           com_to_sub_dict=com_to_sub_dict
                           )


@matlab_bp.route('/4ch')
def four_chapter():
    a_id = 9
    chap_num = 4
    article, user_comment, com_to_sub_dict = get_data(a_id)
    return render_template('matlab/MATLAB_ch4.html',
                           chap_num=chap_num + 1,
                           article=article,
                           user_comment=user_comment,
                           com_to_sub_dict=com_to_sub_dict
                           )


app.register_blueprint(matlab_bp)
