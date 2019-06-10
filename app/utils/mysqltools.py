import pymysql
from config import db_config

def query(sql=''):
    '''
    用法：query('select * from t_user;')\n
    说明：查询数据库工具,返回查询结果
    '''
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


def commit(sql=''):
    '''
    用法：commit('insert into t_user (id,username) values (1,'张三');')\n
    说明：更改数据库工具，支持插入、修改、删除
    '''
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        return True
    except:
        return False

