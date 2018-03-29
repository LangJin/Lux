# -*- conding:utf-8 -*-
__author__ = "LangJin"
from app import bp
from functools import wraps
from flask import jsonify as json, request, flash, session
from app.common.util_db import query, excute
from app.common.util_date import create_token
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
        return json(get_json(code=-300, msg="权限错误,请先登录!", url="/"))

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
        if len(result) == 1:
            token = create_token()
            session['token'] = token
            session["admin"] = result
            excute("UPDATE `tbl_admin` SET `token`='%s' WHERE (`id`='%d') LIMIT 1" % (token, result[0][0]))
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
    return json(get_json(data=_get_admin_session()))



# todo 文章管理 增加 修改 删除 查询

@bp.route("/queryAllArticles/")
@_admin_permission_required
def query_all_articles():
    """
    查询所有文章
    :return: json
    """
    query_articles_sql = "select * from tbl_article order by createDate desc"
    return json(get_json(data=query(query_articles_sql)))


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
        "obj":[                                                 # 返回数据对象
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
                "show_shouye_status":0                          # 是否显示首页，0为不显示
            },
            {
                "total":3                                       # 共有几页
            }
        ],
        "url":""                                                操作成功后需要跳转的链接
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
        'show_shouye_status': show_shouye_status,
        'dic_list': dic                             # 下一页或下下一页的参数的循环参数（开始，结束） 在python中表示 range
    }

    return json(get_json(data=[datas]))


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

    return json(get_json(data=query(conditions_sql)))


@bp.route("/updateArticle/", methods=["POST"])
@_admin_parameters_filter
def update_article():
    return json(get_json())


