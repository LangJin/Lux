# -*- coding:utf-8 -*-
__author__ = 'snake'


import pymysql.cursors
import config as cf
from copy import copy



def query(sql=""):
    """
        根据sql查询结果
        args: sql
        return: results 返回结果(1,"test")
    """
    results = []
    db = pymysql.connect(**cf.db_config)
    cur = db.cursor()
    try:
        cur.execute(sql)  # 执行sql语句
        results = copy(cur.fetchall())  # 获取查询的所有记录
    except Exception as e:
        raise e
    finally:
        cur.close()
        db.close()  # 关闭连接
        return results


"""
    根据sql插入或更新数据
    args: sql
    return: is_success，1:成功 0失败
"""
def excute(sql=""):
    is_success = 1
    db = pymysql.connect(**cf.db_config)
    cur = db.cursor()
    try:
        cur.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        is_success = 0
    finally:
        cur.close()
        db.close()
        return is_success


"""
    执行多条插入或更新语句，级联提交时可使用此方法
    args: [sql1, sql2,...]
    return: is_success，1:成功 0失败
"""
def excutemany(sqls=[]):
    is_success = 1
    db = pymysql.connect(**cf.db_config)
    cur = db.cursor()
    try:
        for sql in sqls:
            cur.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        is_success = 0
    finally:
        cur.close()
        db.close()
        return is_success



if __name__ == "__main__":

    data = query("select * from tbl_test")
    print(data)

    # 测试单条insert
    # name = "test4"
    # sql = "insert into tbl_test values(NULL,'%s')" % name
    # flag = excute(sql)
    # print(flag)
    #
    # 测试单条update
    # name = "update test"
    # sql = "update tbl_test set name='%s' where id=2" % name
    # flag = excute(sql)
    # print(flag)

    #  测试多条update
    # name = "update test"
    # sql1 ="update tbl_test set name='%s' where id=2" % name
    # sql2 ="update tbl_test set name='%s' where id=3" % name
    # print(excute_many([sql1, sql2]))

    #  测试多条insert
    # name = "insert test"
    # sql1 = "insert into tbl_test values(NULL,'%s')" % name
    # sql2 = "insert into tbl_test values(NULL,'%s')" % name
    # print(excutemany([sql1, sql2]))