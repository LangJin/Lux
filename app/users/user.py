# -*- coding:utf-8 -*-
__author__ = 'LangJin'

from flask import jsonify,session,request
from . import userbp
from ..utils.mysqltools import query,commit
from ..utils.othertools import create_token,encryption


@userbp.route("/login",methods=["post"])
def userlogin():
    userinfo = request.get_json()
    username = userinfo.get("username")
    password = userinfo.get("password")
    sql = "select * from t_user where username = '{}'".format(username)
    res = query(sql)
    data = {}
    if len(res) != 1:
        data["msg"] = "数据异常或者用户不存在！"
        data["data"] = None
    else:
        password = encryption(username,password,"user")
        if password == res[0].get("password"):
            token = create_token()
            sql = "update t_user set token = '{token}' where id = {id};".format(token=token,id=res[0].get("id"))
            msg = commit(sql)
            session.clear()
            session["username"] = username
            session["token"] = token
            data["msg"] = "登录成功！"
            data["data"] = {}
            data["data"]["token"] = token
            data["data"]["status"] = msg
        else:
            data["msg"] = "密码错误！"
    return jsonify(data)


