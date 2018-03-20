# -*- coding:utf-8 -*-
__author__ = 'snake'
from datetime import datetime


"""
    获取当前时间
    renturn ："2018-03-20 17:30:56"
"""
def get_datetime_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

