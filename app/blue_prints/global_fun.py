# -*- coding: utf-8 -*-
from app import app
from ..models import *


def get_data(a_id):
    article = Article.query.filter_by(id=a_id).first()
    comment = Comment.query.filter_by(article_id=article.id).all()
    if not comment:
        user_comment = None
        com_to_sub_dict = None
    else:
        # sub_comment_all is like [[<SubComment from parent_comment1, content=None.], []]
        sub_comment_all = [SubComment.query.filter_by(main_comment_id=com.id).all() for com in comment]
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

        for com in comment:
            com_to_sub_dict[com.id] = all_sub_list[_num]
            _num += 1
        # com_to_sub_dict =
        # {parent_comment_1: [(sub_user1, sub_comment1), (sub_user2, sub_comment2)], parent_comment_2: []}

        user = [User.query.filter_by(id=com.user_id).first() for com in comment]
        user_comment = zip(user, comment)

    return article, user_comment, com_to_sub_dict
