# -*- conding:utf-8 -*-
__author__ = "LangJin"
from app import bp
from flask import jsonify, request, flash, session
from app.common.util_db import query, excute
from app.common.util_date import create_token


@bp.route("/adminlogin", methods=["post"])
def adminlogin():
    '''
    管理员登陆
    arg:{"username":"admin","password":"a123456"}
    return: json
    '''
    admininfo = request.get_json()
    username = admininfo["username"]
    password = admininfo["password"]
    if username != None and password != None:
        result = query("SELECT * FROM tbl_admin where username = '%s' and password = '%s';" % (username, password))
        if len(result) == 1:
            token = create_token()
            # session(token)
            excute("UPDATE `tbl_admin` SET `token`='%s' WHERE (`id`='%d') LIMIT 1" % (token, result[0][0]))
            response = {}
            response["code"] = 200
            response["data"] = {"token":token}
            response["msg"] = "登陆成功！"
            return jsonify(response)
        else:
            response = {}
            response["code"] = 200
            response["data"] = 0
            response["msg"] = "账号或者密码错误！"
            return jsonify(response)
    else:
        response = {}
        response["code"] = 200
        response["data"] = 0
        response["msg"] = "账号或者密码不能为空。"
        return jsonify(response)
