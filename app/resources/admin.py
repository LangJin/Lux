# -*- conding:utf-8 -*-
__author__ = "snake"

from app import bp
from functools import wraps
from flask import jsonify as json, request, flash, session
from app.common.util_db import query, excute
from app.common.util_date import create_token, get_current_time
from app.common.util_json import get_json

import math


def _admin_permission_required(func):
    """
    登陆装饰器
    :param func:
    :return: json
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("admin"):
            return func(*args, **kwargs)
        return json(get_json(code=-300, msg="权限错误,请先登录!"))

    return wrapper


def _admin_parameters_filter(paras):
    """
    参数过滤，过滤条件为None或者""
    :param paras: []
    :return: False:不通过;True:通过
    """
    for para in paras:
        if para is None or para == "":
            return False
    return True


def _get_admin_session():
    """
    获取admin的session，内容为admin的数据库信息
    :return: session
    """
    return session.get("admin")


def _set_admin_session(admin):
    """
    设置admin的session，内容为admin的数据库信息
    :param user: admin数据库信息
    :return:
    """
    session.clear()
    session["admin"] = admin


@bp.route("/adminLogin/", methods=["post"])
def adminlogin():
    '''
    管理员登陆
    arg:{"username":"admin","password":"a123456"}
    return: json
    '''
    admininfo = request.get_json()
    username = admininfo["username"]
    password = admininfo["password"]
    if username != None and password != None:
        result = query("SELECT * FROM tbl_admin where username = '%s' and password = '%s';" % (username, password))
        if result:
            token = create_token()
            session['token'] = token
            _set_admin_session(result[0])
            excute("UPDATE `tbl_admin` SET `token`='%s' WHERE (`id`='%d') LIMIT 1" % (token, result[0].get("id")))
            response = {}
            response["code"] = 200
            response["data"] = {"token":token}
            response["msg"] = "登陆成功！"
            return json(response)
        else:
            response = {}
            response["code"] = 200
            response["data"] = 0
            response["msg"] = "账号或者密码错误！"
            return json(response)
    else:
        response = {}
        response["code"] = 200
        response["data"] = 0
        response["msg"] = "账号或者密码不能为空。"
        return json(response)


@bp.route('/adminLogout/')
def logout():
    # 如果会话中有用户名就删除它。
    # 同时从客户端浏览器中删除 session的 name属性
    session.pop('token', None)
    response = {}
    response["code"] = 200
    response["data"] = 1
    response["msg"] = "退出登陆"
    return json(response)


@bp.route("/adminIndex/")
@_admin_permission_required
def admin_index():
    """
    管理员首页
    :return:
    """
    return json(get_json(data={"admin_info":_get_admin_session()}))


# todo 文章管理 增加 修改 删除 查询
@bp.route("/queryAllArticles/")
@_admin_permission_required
def query_all_articles():
    """
    查询所有文章
    :return: json
    """
    query_articles_sql = "select * from tbl_article order by createDate desc"
    datas = {"articles": query(query_articles_sql)}
    return json(get_json(data=datas))


def _get_page(total, p):
    """
    计算分页方法
    :param total: 总数
    :param p: 当前第几页
    :return:
    """
    show_page = 5  # 显示的页码数
    pageoffset = 2  # 偏移量
    start = 1  # 分页条开始
    end = total  # 分页条结束

    if total > show_page:
        if p > pageoffset:
            start = p - pageoffset
            if total > p + pageoffset:
                end = p + pageoffset
            else:
                end = total
        else:
            start = 1
            if total > show_page:
                end = show_page
            else:
                end = total
        if p + pageoffset > total:
            start = start - (p + pageoffset - end)
    # 用于模版中循环
    dic = [start, end+1]
    return dic


@bp.route("/queryPagingArticles/", methods=["POST"])
@_admin_permission_required
def query_paging_articles():
    """
    文章分页查询
    :arg {"page":1}
    :return: json
    详细格式如下，此接口受前端限制，可能会更改
    {
        "code":200                                              # 状态码
        "msg":"ok",                                             # msg
        "data":{                                                 # 返回数据对象
            {"articles":[                                       # 文章列表
                [文章1],[文章2],[文章3],[文章4], ....[文章10]
            ]},
            {
                "current_page":1                                # 当前页码
            },
            {
                "dic_list":[1,4]                                # 通过这个循环来标注下一页 下下一页的参数 例如 articles?p=2;在这里需要post传json格式{"page":1}
            },
            {
                "show_index_status":0                          # 是否显示首页，0为不显示
            },
            {
                "total":3                                       # 共有几页
            }
        }
    }
    """
    paging_info = request.get_json()
    current_page = paging_info.get("page") # 当前页面
    show_shouye_status = 0  # 显示首页状态
    if current_page == '':
        current_page = 1
    else:
        current_page = int(current_page)
        if current_page > 1:
            show_shouye_status = 1

    limit_start = (int(current_page) - 1) * 10

    # 查询n-10*n条记录，首页
    sql = "select * from tbl_article limit %d,10" % limit_start
    article_list = query(sql)

    # 查询总记录和计算总页数
    sql = "select * from tbl_article"
    count = len(query(sql))  # 总记录
    total = int(math.ceil(count / 10.0)) # 总页数

    dic = _get_page(total, current_page)

    datas = {
        "articles": article_list,
        "current_page": int(current_page),
        'total': total,
        'show_index_status': show_shouye_status,
        'show_range': dic                             # 下一页或下下一页的参数的循环参数（开始，结束） 在python中表示 range
    }

    return json(get_json(data=datas))


@bp.route("/queryConditionsArticles/", methods=["POST"])
@_admin_permission_required
def query_conditions_articles():
    """
    多条件联合查询文章
    :arg {"title":"测试","status":1, "source":"测试", "startDate":"2017-03-23 23:59:52", "endDate":"2018-03-28 23:59:52"}
    :return: json
    """
    # 文章title查询、状态查询、来源、创建时间范围查询
    conditions = request.get_json()
    title = conditions.get("title")             # 文章标题
    status = conditions.get("status")           # 状态
    source = conditions.get("source")           # 来源

    end_date = conditions.get("endDate")       # 结束时间
    start_date = conditions.get("startDate")   # 开始时间

    # 开始构造查询语句，分别根据参数是否为空来构造sql语句
    conditions_sql = "select * from tbl_article where 1=1 "
    if _admin_parameters_filter([title]):
        conditions_sql += "and title like '%" + title + "%' "
    if _admin_parameters_filter([status]):
        conditions_sql += "and status=%d " %status
    if _admin_parameters_filter([source]):
        conditions_sql +="and source like '%" + source + "%' "

    # 创建文章的开始和结束时间
    if _admin_parameters_filter([start_date]):
        if _admin_parameters_filter([end_date]):
            conditions_sql += "and createDate > '%s' and createDate < '%s'" % (start_date, end_date)
        else:
            conditions_sql += "and createDate > '%s'" % start_date
    else:
        if _admin_parameters_filter([end_date]):
            conditions_sql += "and createDate < '%s'" % end_date

    datas = {"articles": query(conditions_sql)}
    return json(get_json(data=datas))


@bp.route("/addArticle/", methods=["POST"])
@_admin_permission_required
def add_article():
    article_info = request.get_json()
    title = article_info.get("title")
    img_id = article_info.get("imgId")
    type = article_info.get("type")
    content = article_info.get("content")
    source = article_info.get("source")
    user_id = _get_admin_session().get("id")

    # 参数校验
    if not _admin_parameters_filter([title, img_id, type, content, source]):
        return json(get_json(msg="操作失败，参数有误!"))

    # 插入文章记录
    insert_article_sql = "INSERT INTO tbl_article VALUES(NULL, '%s', %d, %d, '%s', '%s', 0, 0, 1, %d, '%s', NULL)" % (title, img_id, type, content, source, user_id, get_current_time())
    if excute(insert_article_sql):
        return json(get_json())

    return json(get_json(code=-100, msg="操作失败，请检查数据库链接!"))


