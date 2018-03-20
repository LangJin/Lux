# -*- coding:utf-8 -*-
__author__ = 'lux'


def get_json(code=200, msg="OK", data=[], url=""):
    """
        获取指定格式的Json数据
        args:
            code=200
            msg="OK"
            data=[]
            url="/"
        return: {}
    """
    return {"code": code, "msg": msg, "url": url, "obj": data}