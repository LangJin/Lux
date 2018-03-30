# -*- coding:utf-8 -*-
__author__ = 'snake'

import pymysql.cursors
import config as cf
from app.common.util_date import decode_result_date


def query(sql=""):
    """
        根据sql查询结果
        args: sql
        return: results 返回结果[{'articleId': 2, 'status': 1, 'createDate': '2018-03-30 11:22:50', 'userId': -1, 'id': 4, 'updateDate': None}]
    """
    results = []
    db = pymysql.connect(**cf.db_config)
    cur = db.cursor()
    try:
        cur.execute(sql)  # 执行sql语句
        # 获得列名
        descs = []
        for desc in cur.description:
            descs.append(desc[0])

        # 构造键值对{"列名":数据}
        results = []
        for res in decode_result_date(cur.fetchall()):
            row = {}
            for i in range(len(descs)):
                row[descs[i]] = res[i]
            results.append(row)
    except Exception as e:
        raise e
    finally:
        cur.close()
        db.close()  # 关闭连接
        return results


def excute(sql=""):
    """
        根据sql插入或更新数据
        args: sql
        return: is_success，1:成功 0失败
    """
    is_success = True
    db = pymysql.connect(**cf.db_config)
    cur = db.cursor()
    try:
        cur.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        is_success = False
    finally:
        cur.close()
        db.close()
        return is_success


def excutemany(sqls=[]):
    """
        执行多条插入或更新语句，级联提交时可使用此方法
        args: [sql1, sql2,...]
        return: is_success，1:成功 0失败
    """

    is_success = True
    db = pymysql.connect(**cf.db_config)
    cur = db.cursor()
    try:
        for sql in sqls:
            cur.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        is_success = False
    finally:
        cur.close()
        db.close()
        return is_success


if __name__ == "__main__":
    data = query("select * from tbl_user where username='1' and password='1'")
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
