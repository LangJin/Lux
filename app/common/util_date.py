# -*- coding:utf-8 -*-
__author__ = 'snake'
from datetime import datetime



def get_current_time():
    """
        获取当前时间
        renturn ："2018-03-20 17:30:56"
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

