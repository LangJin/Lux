# -*- coding:utf-8 -*-
__author__ = 'snake'


def get_json(code=200, msg="操作成功!", data={}):
    """
        获取指定格式的Json数据
        args:
            code=200
            msg="OK"
            data={}
        return: {}
    """
    return {"code": code, "msg": msg, "data": data}