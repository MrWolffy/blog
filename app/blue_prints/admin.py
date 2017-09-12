# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from app import app
from ..models import User, Role, Article, Comment


admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')



app.register_blueprint(admin_bp)
