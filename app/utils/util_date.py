# -*- coding:utf-8 -*-
__author__ = 'snake'

from datetime import datetime


def decode_result_date(datas):
    """
    将数据库查询的数据进行时间格式化
    :param datas: (())， 从数据库查询的数据
    :return: [[]] 返回list列表
    """
    results = []
    for data in datas:
        tmp_list = []
        for item in data:
            if isinstance(item, datetime):
                tmp_list.append(item.strftime('%Y-%m-%d %H:%M:%S'))
            else:
                tmp_list.append(item)
        results.append(tmp_list)

    return results


def get_current_time():
    """
    获取当前时间
    :renturn:"2018-03-20 17:30:56"
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
