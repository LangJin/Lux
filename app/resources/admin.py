# -*- conding:utf-8 -*-
__author__ = "LangJin"
from app import bp
from flask import jsonify as json, request, flash, session
from app.common.util_db import query, excute
from app.common.util_date import create_token
from app.common.util_json import get_json



@bp.route("/adminLogin/", methods=["post"])
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
            session['token'] = token
            excute("UPDATE `tbl_admin` SET `token`='%s' WHERE (`id`='%d') LIMIT 1" % (token, result[0][0]))
            response = {}
            response["code"] = 200
            response["data"] = {"token":token}
            response["msg"] = "登陆成功！"
            return json(response)
        else:
            response = {}
            response["code"] = 200
            response["data"] = 0
            response["msg"] = "账号或者密码错误！"
            return json(response)
    else:
        response = {}
        response["code"] = 200
        response["data"] = 0
        response["msg"] = "账号或者密码不能为空。"
        return json(response)


@bp.route('/adminLogout/')
def logout():
    # 如果会话中有用户名就删除它。
    # 同时从客户端浏览器中删除 session的 name属性
    session.pop('token', None)
    response = {}
    response["code"] = 200
    response["data"] = 1
    response["msg"] = "退出登陆"
    return json(response)



@bp.route("/adminIndex/")
def admin_index():
    return json(get_json())