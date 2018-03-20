# -*- coding:utf-8 -*-
__author__ = 'lux'


def get_json(code=200, msg="OK", data=[], url=""):
    return {"code": code, "msg": msg, "url": url, "obj": data}