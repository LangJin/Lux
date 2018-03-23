# -*- conding:utf-8 -*-
__author__ = "LangJin"
from app import bp
from flask import jsonify

@bp.route("/jin")
def jin():
    '''
    测试
    '''
    return jsonify(["1111"])
