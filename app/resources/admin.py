# -*- conding:utf-8 -*-
__author__ = "snake"

from app import bp
from functools import wraps
from flask import jsonify as json, request, session
from app.utils.util_db import query, excute
from app.utils.util_date import get_current_time
from app.utils.util_token import create_token
from app.utils.util_json import get_json

import math, traceback


def _admin_permission_required(func):
    """
    登陆装饰器
    :param func:
    :return: json
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.get_json().get("token")
        if token is not None and token != ""\
                and token == session.get("admin_token"):
            try:
                return func(*args, **kwargs)
            except:
                print(traceback.print_exc())
                return json(get_json(code=500, msg="内部错误,请检查参数是否正确!"))
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
    返回不包含password和token的user信息和token信息
    :return: {"adminInfo":{}, "token":"Xxx"}
    """

    from copy import copy
    admin = copy(session.get("admin"))
    admin.pop("token", None)
    admin.pop("password", None)

    return {"adminInfo": admin}



def _set_admin_session(admin):
    """
    设置admin的session，内容为admin的数据库信息
    :param user: admin数据库信息
    :return:
    """
    session.clear()
    session["admin"] = admin
    session["admin_token"] = admin.get("token")


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
    dic = [start, end + 1]
    return dic


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
            result[0]["token"] = token
            _set_admin_session(result[0])
            excute("UPDATE `tbl_admin` SET `token`='%s' WHERE (`id`='%d') LIMIT 1" % (token, result[0].get("id")))
            response = {}
            response["code"] = 200
            response["data"] = {"token": token}
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
    session.pop('admin', None)
    response = {}
    response["code"] = 200
    response["data"] = 1
    response["msg"] = "退出登陆"
    return json(response)


@bp.route("/adminIndex/", methods=["post"])
@_admin_permission_required
def admin_index():
    """
    管理员首页
    :args {"token":"xxx}
    :return:
    """
    return json(get_json(data=_get_admin_session()))


@bp.route("/queryAllArticles/", methods=["post"])
@_admin_permission_required
def query_all_articles():
    """
    查询所有文章
    :args {"token": "hq1bjvcc-o4ub-dwlv-1uok-lhmixq5lvkl3"}
    :return: json
    """
    query_articles_sql = "select * from tbl_article order by createDate desc"
    datas = {
        "articles": query(query_articles_sql)
    }
    return json(get_json(data=datas))


@bp.route("/queryPagingArticles/", methods=["POST"])
@_admin_permission_required
def query_paging_articles():
    """
    文章分页查询
    :arg {"page":1,"token": "lup5gvda-5vwa-q3yp-kub5-sz69v6qxtgr3"}
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
    current_page = paging_info.get("page")  # 当前页面
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
    total = int(math.ceil(count / 10.0))  # 总页数

    dic = _get_page(total, current_page)

    datas = {
        "articles": article_list,
        "current_page": int(current_page),
        'total': total,
        'show_index_status': show_shouye_status,
        'show_range': dic  # 下一页或下下一页的参数的循环参数（开始，结束） 在python中表示 range
    }

    return json(get_json(data=datas))


@bp.route("/queryConditionsArticles/", methods=["POST"])
@_admin_permission_required
def query_conditions_articles():
    """
    多条件联合查询文章
    :arg :
    {
    "title":"测试","status":1, "source":"测试",
    "startDate":"2017-03-23 23:59:52", "endDate":"2018-03-28 23:59:52",
    "token": "x8txta6o-rbmx-sc43-6hc4-u0prik5s8yay"
    }
    :return: json
    """
    # 文章title查询、状态查询、来源、创建时间范围查询
    conditions = request.get_json()
    title = conditions.get("title")  # 文章标题
    status = conditions.get("status")  # 状态
    source = conditions.get("source")  # 来源

    end_date = conditions.get("endDate")  # 结束时间
    start_date = conditions.get("startDate")  # 开始时间

    # 开始构造查询语句，分别根据参数是否为空来构造sql语句
    conditions_sql = "select * from tbl_article where 1=1 "
    if _admin_parameters_filter([title]):
        conditions_sql += "and title like '%" + title + "%' "
    if _admin_parameters_filter([status]):
        conditions_sql += "and status=%d " % status
    if _admin_parameters_filter([source]):
        conditions_sql += "and source like '%" + source + "%' "

    # 创建文章的开始和结束时间
    if _admin_parameters_filter([start_date]):
        if _admin_parameters_filter([end_date]):
            conditions_sql += "and createDate > '%s' and createDate < '%s'" % (start_date, end_date)
        else:
            conditions_sql += "and createDate > '%s'" % start_date
    else:
        if _admin_parameters_filter([end_date]):
            conditions_sql += "and createDate < '%s'" % end_date

    datas = {
        "articles": query(conditions_sql)
    }
    return json(get_json(data=datas))


@bp.route("/addArticle/", methods=["POST"])
@_admin_permission_required
def add_article():
    """
    新增文章
    :arg
    {
    "title":"title", "imgId":1,"type":2, "content":"test", "source":"123","token": "6gax71xs-z38o-8178-3a2t-6c3jjcm2cn18"
    }
    :return: json
    """
    article_info = request.get_json()
    type = article_info.get("type")
    title = article_info.get("title")
    img_id = article_info.get("imgId")
    source = article_info.get("source")
    content = article_info.get("content")
    user_id = _get_admin_session()["adminInfo"]["id"]

    # 参数校验
    if not _admin_parameters_filter([title, img_id, type, content, source]):
        return json(get_json(code=-200, msg="操作失败，参数有误!"))

    # 插入文章记录
    insert_article_sql = "INSERT INTO tbl_article VALUES" \
                         "(NULL, '%s', %d, %d, '%s', '%s', 0, 0, 1, %d, '%s', NULL)" % \
                         (title, img_id, type, content, source, user_id, get_current_time())
    if excute(insert_article_sql):
        return json(get_json())

    return json(get_json(code=-100, msg="操作失败，请检查数据库链接!"))


@bp.route("/updateArticle/", methods=["POST"])
@_admin_permission_required
def update_article():
    """
    更新文章
    :arg
    {
        "id":1, "type":1, "title":"title_test",
        "source":"1", "status":1, "content":"test_test",
        "imgId":1,"token": "75wglrvu-uiol-ifza-73c9-d9vu4e5sql0m"
    }
    :return:
    """
    article_info = request.get_json()
    id = article_info.get("id")
    type = article_info.get("type")
    title = article_info.get("title")
    img_id = article_info.get("imgId")
    source = article_info.get("source")
    status = article_info.get("status")
    content = article_info.get("content")

    # 参数校验
    if not _admin_parameters_filter([id, status, title, type, content, source, img_id]):
        return json(get_json(code=-200, msg="操作失败，参数有误!"))

    # 更新文章
    update_article_sql = "update tbl_article set " \
                         "title='%s', type=%d, source='%s', status=%d, content='%s', updateDate='%s', imgId='%d'" \
                         "where id=%d" % (title, type, source, status, content, get_current_time(), img_id, id)
    if excute(update_article_sql):
        return json(get_json(msg="更新成功!"))

    return json(get_json(code=-100, msg="操作失败，请检查数据库链接!"))


@bp.route("/deleteArticle/", methods=["POST"])
@_admin_permission_required
def delete_article():
    """
    删除文章(软删除)
    :arg {"id":1, "token":"dd0tl9ek-v65c-un69-v450-vdjxweucf0f7"}
    :return:
    """
    article_info = request.get_json()
    id = article_info.get("id")

    # 参数校验
    if not _admin_parameters_filter([id]):
        return json(get_json(code=-200, msg="操作失败，参数有误!"))

    # 更新文章
    update_article_sql = "update tbl_article set status=0 where id=%d" % id
    if excute(update_article_sql):
        return json(get_json(msg="删除成功!"))

    return json(get_json(code=-100, msg="操作失败，请检查数据库链接!"))


@bp.route("/activeArticle/", methods=["POST"])
@_admin_permission_required
def active_article():
    """
    激活已删除的文章
    :arg {"id":1, "token":"dd0tl9ek-v65c-un69-v450-vdjxweucf0f7"}}
    :return:
    """
    article_info = request.get_json()
    id = article_info.get("id")

    # 参数校验
    if not _admin_parameters_filter([id]):
        return json(get_json(code=-200, msg="操作失败，参数有误!"))

    # 更新文章
    update_article_sql = "update tbl_article set status=1 where id=%d" % id
    if excute(update_article_sql):
        return json(get_json(msg="激活文章成功!"))

    return json(get_json(code=-100, msg="操作失败，请检查数据库链接!"))


@bp.route("/queryAllUsers/", methods=["post"])
@_admin_permission_required
def query_all_users():
    """
    查询所有用户
    :args {"token": "ol5r2k0p-0fn0-kbyd-1xpe-zq4n6sgk5wa5"}
    :return: json
    """
    query_users_sql = "select * from tbl_user"
    datas = {"users": query(query_users_sql)}
    return json(get_json(data=datas))


@bp.route("/queryPagingAUsers/", methods=["POST"])
@_admin_permission_required
def query_paging_users():
    """
    用户分页查询
    :arg {"page":2,"token": "te4uzdia-gkee-ziiy-5cjg-zz8qji20z7a6"}
    :return: json
    详细格式如下，此接口受前端限制，可能会更改
    {
        "code":200                                              # 状态码
        "msg":"ok",                                             # msg
        "data":{                                                 # 返回数据对象
            {"articles":[                                       # 文章列表
                [用户1],[用户2],[用户3],[用户4], ....[用户10]
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
    current_page = paging_info.get("page")  # 当前页面
    show_shouye_status = 0  # 显示首页状态
    if current_page == '':
        current_page = 1
    else:
        current_page = int(current_page)
        if current_page > 1:
            show_shouye_status = 1

    limit_start = (int(current_page) - 1) * 10

    # 查询n-10*n条记录，首页
    sql = "select * from tbl_user limit %d,10" % limit_start
    user_list = query(sql)

    # 查询总记录和计算总页数
    sql = "select * from tbl_user"
    count = len(query(sql))  # 总记录
    total = int(math.ceil(count / 10.0))  # 总页数

    dic = _get_page(total, current_page)

    datas = {
        "users": user_list,
        "currentPage": int(current_page),
        'total': total,
        'showIndexStatus': show_shouye_status,
        'showRange': dic  # 下一页或下下一页的参数的循环参数（开始，结束） 在python中表示 range
    }

    return json(get_json(data=datas))


@bp.route("/queryConditionsUsers/", methods=["POST"])
@_admin_permission_required
def query_conditions_users():
    """
    多条件联合查询用户
    :arg
    {
        "username":"user1","nickname":"user, "status":1, "sex":"男",
        "email":"test@qq.com", "phone_num":"15000000000", "wechat":1,
        "startDate":"2017-03-23 23:59:52", "endDate":"2018-03-28 23:59:52",
        "token": "te4uzdia-gkee-ziiy-5cjg-zz8qji20z7a6"
    }
    :return: json
    """
    # 文章title查询、状态查询、来源、创建时间范围查询
    conditions = request.get_json()
    username = conditions.get("username")  # 用户名
    nickname = conditions.get("nickname")  # 昵称
    status = conditions.get("status")  # 状态
    sex = conditions.get("sex")  # 性别
    email = conditions.get("email")  # 邮箱
    phone_num = conditions.get("cellphone")  # 电话
    wechat = conditions.get("wechat")  # 微信号

    end_date = conditions.get("endDate")  # 结束时间
    start_date = conditions.get("startDate")  # 开始时间

    # 开始构造查询语句，分别根据参数是否为空来构造sql语句
    conditions_sql = "select * from tbl_user where 1=1 "
    if _admin_parameters_filter([username]):
        conditions_sql += "and username like '%" + username + "%' "
    if _admin_parameters_filter([nickname]):
        conditions_sql += "and nickname like '%" + nickname + "%' "
    if _admin_parameters_filter([status]):
        conditions_sql += "and status=%d " % status
    if _admin_parameters_filter([sex]):
        conditions_sql += "and sex='%s' " % sex
    if _admin_parameters_filter([email]):
        conditions_sql += "and email like '%" + email + "%' "
    if _admin_parameters_filter([phone_num]):
        conditions_sql += "and phone_num like '%" + phone_num + "%' "
    if _admin_parameters_filter([wechat]):
        conditions_sql += "and wechat like '%" + wechat + "%' "

    # 创建文章的开始和结束时间
    if _admin_parameters_filter([start_date]):
        if _admin_parameters_filter([end_date]):
            conditions_sql += "and createDate > '%s' and createDate < '%s'" % (start_date, end_date)
        else:
            conditions_sql += "and createDate > '%s'" % start_date
    else:
        if _admin_parameters_filter([end_date]):
            conditions_sql += "and createDate < '%s'" % end_date
    datas = {"users": query(conditions_sql)}
    return json(get_json(data=datas))


@bp.route("/addUser/", methods=["POST"])
@_admin_permission_required
def add_user():
    """
    新增用户
    :arg {"username":"user", "password":"123", "nickname":"nickname", "token": "4cmhr7a8-t0zw-sskr-3e5i-o9sdxv48878p"}
    :return: json
    """
    user_info = request.get_json()
    nickname = user_info.get("nickname")
    username = user_info.get("username")
    password = user_info.get("password")
    create_date = get_current_time()

    # 参数校验
    if not _admin_parameters_filter([username, password, nickname]):
        return json(get_json(code=-200, msg="参数存在空值，请检查参数!"))

    # 判断用户名是否已被占用
    query_user_sql = "select * from tbl_user where username='%s'" % username
    if query(query_user_sql):
        return json(get_json(code=-300, msg="用户名已存在!"))

    # 没被占用，进行注册
    user_reg_sql = "insert into tbl_user values" \
                   "(NULL, '%s', '%s', '%s',NULL,1,'','','',NULL,'','','','',NULL,'','%s',NULL)" \
                   % (username, password, nickname, create_date)
    print(user_reg_sql)
    if excute(user_reg_sql):
        return json(get_json(msg="新增用户成功!"))

    return json(get_json(code=-100, msg="新增用户失败!"))


@bp.route("/updateUser/", methods=["POST"])
@_admin_permission_required
def update_user():
    """
    编辑用户信息
    :arg {
    "id":1, "status":1, "sex":"男",
    "age":22, "email":"test@qq.com",
    "wechat":"snake", "remark":"greate full!",
    "address":"test", "nickname":"snake",
    "signature":"signature", "cellphone":"15000000000",
    "education":"education","token": "4cmhr7a8-t0zw-sskr-3e5i-o9sdxv48878p"
    }
    :return: json
    """
    user_info = request.get_json()
    id = user_info.get("id")
    sex = user_info.get("sex")
    age = user_info.get("age")
    email = user_info.get("email")
    status = user_info.get("status")
    wechat = user_info.get("wechat")
    remark = user_info.get("remark")
    address = user_info.get("address")
    nickname = user_info.get("nickname")
    signature = user_info.get("signature")
    cellphone = user_info.get("cellphone")
    education = user_info.get("education")
    updateDate = get_current_time()

    # 执行用户信息更新
    update_user_sql = "update tbl_user set nickname='%s'," \
                      "sex='%s',age=%d, email='%s', wechat='%s'," \
                      "remark='%s',address='%s',nickname='%s'," \
                      "signature='%s',cellphone='%s',education='%s'," \
                      "updateDate='%s',status=%d where id='%s'" % \
                      (nickname, sex, age, email, wechat, remark, address, \
                       nickname, signature, cellphone, education, updateDate,
        status, id)
    # 更新成功则重置session并返回最新的用户信息
    if excute(update_user_sql):
        return json(get_json(msg="修改成功!"))

    return json(get_json(code=-100, msg="修改失败!"))


@bp.route("/defriendUser/", methods=["POST"])
@_admin_permission_required
def defriend_user():
    """
    拉黑用户
    :arg {"id":1,"token": "2fvblixe-mxqg-weu5-mvqo-48ick796k009"}
    :return:
    """
    user_info = request.get_json()
    id = user_info.get("id")

    # 参数校验
    if not _admin_parameters_filter([id]):
        return json(get_json(code=-200, msg="操作失败，参数有误!"))

    # 更新文章
    update_article_sql = "update tbl_user set status=0 where id=%d" % id
    if excute(update_article_sql):
        return json(get_json(msg="拉黑成功, 该用户被禁止登陆网站!"))  # todo 这里有bug，不能及时踢下线，哈哈哈

    return json(get_json(code=-100, msg="操作失败，请检查数据库链接!"))


@bp.route("/recoverUser/", methods=["POST"])
@_admin_permission_required
def recover_user():
    """
    恢复用户
    :arg {"id":1,"token": "2fvblixe-mxqg-weu5-mvqo-48ick796k009"}
    :return:
    """
    user_info = request.get_json()
    id = user_info.get("id")

    # 参数校验
    if not _admin_parameters_filter([id]):
        return json(get_json(code=-200, msg="操作失败，参数有误!"))

    # 更新文章
    update_article_sql = "update tbl_user set status=1 where id=%d" % id
    if excute(update_article_sql):
        return json(get_json(msg="恢复成功, 该用户可以登陆网站!"))

    return json(get_json(code=-100, msg="操作失败，请检查数据库链接!"))


@bp.route("/queryAllUserComments/", methods=["post"])
@_admin_permission_required
def query_all_user_comments():
    """
    查询所有用户文章及评论
    :arg {"token": "2fvblixe-mxqg-weu5-mvqo-48ick796k009"}
    :return: cId,cUserId ... = comment表中的数据，重命名comments表是为了防止查询的字段冲突不显示
    """
    query_all_user_comments_sql = "select b.*," \
                                  "a.id as cId," \
                                  "a.userId as cUserId, " \
                                  "a.articleId as cArticleId, " \
                                  "a.content as cContent, " \
                                  "a.status as cStatus, " \
                                  "a.createDate as cCreateDate," \
                                  "a.updateDate as cUpdateDate, " \
                                  "a.fid as cFid " \
                                  "from tbl_article_comment as a join tbl_article as b where a.articleId=b.id"

    comments = {"articlesAndComments": query(query_all_user_comments_sql)}

    return json(get_json(data=comments))


@bp.route("/queryPagingComments/", methods=["POST"])
@_admin_permission_required
def query_paging_comments():
    """
    用户分页查询
    :arg {"page":1}
    :return: json
    详细格式如上述接口
    """
    paging_info = request.get_json()
    current_page = paging_info.get("page")  # 当前页面
    show_shouye_status = 0  # 显示首页状态
    if current_page == '':
        current_page = 1
    else:
        current_page = int(current_page)
        if current_page > 1:
            show_shouye_status = 1

    limit_start = (int(current_page) - 1) * 10

    # 查询n-10*n条记录，首页
    sql = "select a.*, " \
          "b.content as aContent " \
          "from tbl_article_comment as a join tbl_article as b " \
          "where a.articleId = b.id limit %d,10" % limit_start
    comments_list = query(sql)

    # 查询总记录和计算总页数
    sql = "select a.*, " \
          "b.content as aContent " \
          "from tbl_article_comment as a join tbl_article as b " \
          "where a.articleId = b.id"
    count = len(query(sql))  # 总记录
    total = int(math.ceil(count / 10.0))  # 总页数

    dic = _get_page(total, current_page)

    datas = {
        "comments": comments_list,
        "currentPage": int(current_page),
        'total': total,
        'showIndexStatus': show_shouye_status,
        'showRange': dic  # 下一页或下下一页的参数的循环参数（开始，结束） 在python中表示 range
    }

    return json(get_json(data=datas))


@bp.route("/queryConditionsComments/", methods=["POST"])
@_admin_permission_required
def query_conditions_comments():
    """
    多条件联合查询评论
    :arg {"aContent":"测试", "cContent":"文章", "status":1, "startDate":"2017-03-23 23:59:52", "endDate":"2018-03-28 23:59:52"}
    :return: json
    """
    # 文章名字 评论内容 评论状态 创建时间
    conditions = request.get_json()
    status = conditions.get("status")
    article_content = conditions.get("aContent")
    comment_content = conditions.get("cContent")
    end_date = conditions.get("endDate")  # 结束时间
    start_date = conditions.get("startDate")  # 开始时间

    # 开始构造查询语句，分别根据参数是否为空来构造sql语句
    conditions_sql = "select a.*, b.content as aContent from tbl_article_comment as a join tbl_article as b where 1=1 "
    if _admin_parameters_filter([status]):
        conditions_sql += "and a.status=%d " % status
    if _admin_parameters_filter([article_content]):
        conditions_sql += "and b.content like '%"+article_content+"%' "
    if _admin_parameters_filter([comment_content]):
        conditions_sql += "and a.content like '%"+comment_content+"%' "

    # 创建文章的开始和结束时间
    if _admin_parameters_filter([start_date]):
        if _admin_parameters_filter([end_date]):
            conditions_sql += "and a.createDate > '%s' and a.createDate < '%s'" % (start_date, end_date)
        else:
            conditions_sql += "and a.createDate > '%s'" % start_date
    else:
        if _admin_parameters_filter([end_date]):
            conditions_sql += "and a.createDate < '%s'" % end_date

    datas = {"comments": query(conditions_sql)}
    return json(get_json(data=datas))


@bp.route("/defriendComment/", methods=["POST"])
@_admin_permission_required
def defriend_comment():
    """
    禁止显示文章的评论
    :arg {"id": 1, "token":"3dfvjaj0-81hp-gwzl-wub9-2qsllamg2mou"}
    :return: json
    """
    comment_info = request.get_json()
    id = comment_info.get("id")

    # 参数校验
    if not _admin_parameters_filter([id]):
        return json(get_json(code=-200, msg="操作失败，参数有误!"))

    # 更新评论记录
    update_comment_sql = "update tbl_article_comment set status = 0 where id=%d" % id
    if excute(update_comment_sql):
        return json(get_json(msg="评论已设置为不显示!"))

    return json(get_json(code=-100, msg="操作失败，请检查数据库链接!"))


@bp.route("/recoverComment/", methods=["POST"])
@_admin_permission_required
def recover_comment():
    """
    恢复显示文章的评论
    :arg {"id": 1, "token":"3dfvjaj0-81hp-gwzl-wub9-2qsllamg2mou"}
    :return: json
    """
    comment_info = request.get_json()
    id = comment_info.get("id")

    # 参数校验
    if not _admin_parameters_filter([id]):
        return json(get_json(code=-200, msg="操作失败，参数有误!"))

    # 更新评论记录
    update_comment_sql = "update tbl_article_comment set status = 1 where id=%d" % id
    if excute(update_comment_sql):
        return json(get_json(msg="评论已设置为显示!"))

    return json(get_json(code=-100, msg="操作失败，请检查数据库链接!"))


@bp.route("/queryAllAnnos/",methods=["post"])
@_admin_permission_required
def query_all_announcements():
    """
    查询所有跑马灯公告:
    arg {"token": "qzh84z4m-vsl7-ltkq-6xzq-wur2tkts2ppw"}
    :return: json
    """
    query_all_anno_sql = "select a.*, " \
                         "b.username as adminName " \
                         "from tbl_announcement as a JOIN tbl_admin as b where a.userId=b.id"
    annos = {"announcements": query(query_all_anno_sql)}
    return json(get_json(data=annos))


@bp.route("/queryPagingAnnos/", methods=["POST"])
@_admin_permission_required
def query_paging_annos():
    """
    公告分页查询
    :arg {"page":1}
    :return: json
    详细格式如上述接口
    """
    paging_info = request.get_json()
    current_page = paging_info.get("page")  # 当前页面
    show_shouye_status = 0  # 显示首页状态
    if current_page == '':
        current_page = 1
    else:
        current_page = int(current_page)
        if current_page > 1:
            show_shouye_status = 1

    limit_start = (int(current_page) - 1) * 10

    # 查询n-10*n条记录，首页
    sql = "select a.*," \
          " b.username as adminName " \
          "from tbl_announcement as a JOIN tbl_admin as b where a.userId=b.id limit %d,10" % limit_start
    annos_list = query(sql)

    # 查询总记录和计算总页数
    sql = "select a.*, " \
          "b.username as adminName " \
          "from tbl_announcement as a JOIN tbl_admin as b where a.userId=b.id"
    count = len(query(sql))  # 总记录
    total = int(math.ceil(count / 10.0))  # 总页数

    dic = _get_page(total, current_page)

    datas = {
        "comments": annos_list,
        "currentPage": int(current_page),
        'total': total,
        'showIndexStatus': show_shouye_status,
        'showRange': dic  # 下一页或下下一页的参数的循环参数（开始，结束） 在python中表示 range
    }

    return json(get_json(data=datas))


@bp.route("/queryConditionsAnnos/", methods=["POST"])
@_admin_permission_required
def query_conditions_annos():
    """
    多条件联合查询公告
    :arg {
        "token": "qzh84z4m-vsl7-ltkq-6xzq-wur2tkts2ppw",
        "title":"公告", "status":1, "username":"admin1",
        "startDate":"2017-03-23 23:59:52", "endDate":"2018-04-28 23:59:52"
    }
    :return: json
    """
    # 公告标题 状态 开始时间 结束时间
    conditions = request.get_json()
    title = conditions.get("title")
    status = conditions.get("status")
    create_user = conditions.get("username")
    end_date = conditions.get("endDate")  # 结束时间
    start_date = conditions.get("startDate")  # 开始时间

    # 开始构造查询语句，分别根据参数是否为空来构造sql语句
    conditions_sql = "select a.*, " \
                     "b.username as adminName " \
                     "from tbl_announcement as a JOIN tbl_admin as b where a.userId=b.id "
    if _admin_parameters_filter([title]):
        conditions_sql += "and a.title like '%"+title+"%' "
    if _admin_parameters_filter([status]):
        conditions_sql += "and a.status=%d " % status
    if _admin_parameters_filter([create_user]):
        conditions_sql += "and b.username='%s' " % create_user

    # 创建公告的开始和结束时间
    if _admin_parameters_filter([start_date]):
        if _admin_parameters_filter([end_date]):
            conditions_sql += "and a.createDate > '%s' and a.createDate < '%s'" % (start_date, end_date)
        else:
            conditions_sql += "and a.createDate > '%s'" % start_date
    else:
        if _admin_parameters_filter([end_date]):
            conditions_sql += "and a.createDate < '%s'" % end_date

    datas = {"comments": query(conditions_sql)}
    return json(get_json(data=datas))


@bp.route("/addAnno/", methods=["POST"])
@_admin_permission_required
def add_anno():
    """
    增加公告
    :arg {"title":"测试", "content":"测试", "status":1,"token": "qzh84z4m-vsl7-ltkq-6xzq-wur2tkts2ppw"}
    :return:
    """
    anno_info = request.get_json()
    title = anno_info.get("title")
    content = anno_info.get("content")
    status = anno_info.get("status")
    create_date = get_current_time()
    admin_id = _get_admin_session()["adminInfo"]["id"]

    # 参数校验
    if not _admin_parameters_filter([title, content, status]):
        return json(get_json(code=-200, msg="操作失败，参数有误!"))

    # 构造sql并执行
    insert_anno_sql = "INSERT into tbl_announcement " \
                      "values(NULL, '%s', %d, %d, '%s', '%s')" % (content, status, admin_id, create_date, title)
    if excute(insert_anno_sql):
        return json(get_json(msg="添加成功!"))

    return json(get_json(code=-100, msg="添加失败，请检查数据库链接!"))


@bp.route("/updateAnno/", methods=["POST"])
@_admin_permission_required
def update_anno():
    """
    修改公告
    :arg {"id":1, "title":"测试", "content":"测试", "status":1,"token": "qzh84z4m-vsl7-ltkq-6xzq-wur2tkts2ppw"}
    :return:
    """
    anno_info = request.get_json()
    id = anno_info.get("id")
    title = anno_info.get("title")
    content = anno_info.get("content")
    status = anno_info.get("status")

    # 参数校验
    if not _admin_parameters_filter([id, title, content, status]):
        return json(get_json(code=-200, msg="操作失败，参数有误!"))

    # 构造sql并执行
    insert_anno_sql = "update tbl_announcement " \
                      "set title='%s', content='%s', status=%d where id=%d" % (title, content, status, id)
    if excute(insert_anno_sql):
        return json(get_json(msg="修改成功!"))

    return json(get_json(code=-100, msg="修改失败，请检查数据库链接!"))


@bp.route("/deleteAnno/", methods=["POST"])
@_admin_permission_required
def delete_anno():
    """
    删除公告:软删除
    :arg {"id":1,"token": "qzh84z4m-vsl7-ltkq-6xzq-wur2tkts2ppw"}
    :return:
    """
    anno_info = request.get_json()
    id = anno_info.get("id")

    # 参数校验
    if not _admin_parameters_filter([id]):
        return json(get_json(code=-200, msg="操作失败，参数有误!"))

    # 构造参数并执行sql
    delete_anno_sql = "update tbl_announcement set status=0 where id=%d" % id
    if excute(delete_anno_sql):
        return json(get_json(msg="删除成功,该公告将不会在首页显示!"))

    return json(get_json(code=-100, msg="删除失败，请检查数据库链接!"))


@bp.route("/queryAllCarouses/", methods=["post"])
@_admin_permission_required
def query_all_carouses():
    """
    :arg {"token": "qzh84z4m-vsl7-ltkq-6xzq-wur2tkts2ppw"}
    :return:
    """
    query_all_carouses_sql = "select a.*, b.path as imgPath " \
                             "from tbl_carouse as a JOIN tbl_image_sources as b " \
                             "where a.imgId=b.id;"
    datas = {"carouses": query(query_all_carouses_sql)}
    return  json(get_json(data=datas))


@bp.route("/queryPagingCarouses/", methods=["POST"])
@_admin_permission_required
def query_paging_carouses():
    """
    轮播图分页查询
    :arg {"page":1,"token": "mz3ofz13-rgph-sbi9-gg8t-xiemoczr0i9s"}
    :return: json
    详细格式如上述接口
    """
    paging_info = request.get_json()
    current_page = paging_info.get("page")  # 当前页面
    show_shouye_status = 0  # 显示首页状态
    if current_page == '':
        current_page = 1
    else:
        current_page = int(current_page)
        if current_page > 1:
            show_shouye_status = 1

    limit_start = (int(current_page) - 1) * 10

    # 查询n-10*n条记录，首页
    sql = "select a.*, b.path as imgPath  " \
          "from tbl_carouse as a JOIN tbl_image_sources as b where a.imgId=b.id limit %d,10" % limit_start
    carouses_list = query(sql)

    # 查询总记录和计算总页数
    sql = "select a.*, b.path as imgPath from tbl_carouse " \
          "as a JOIN tbl_image_sources as b where a.imgId=b.id"
    count = len(query(sql))  # 总记录
    total = int(math.ceil(count / 10.0))  # 总页数

    dic = _get_page(total, current_page)

    datas = {
        "comments": carouses_list,
        "currentPage": int(current_page),
        'total': total,
        'showIndexStatus': show_shouye_status,
        'showRange': dic  # 下一页或下下一页的参数的循环参数（开始，结束） 在python中表示 range
    }

    return json(get_json(data=datas))


@bp.route("/queryConditionsCarouses/", methods=["POST"])
@_admin_permission_required
def query_conditions_carouses():
    """
    多条件联合查询轮播图
    :arg
    {
        "type":1, "status":1, "startDate":"2017-03-23 23:59:52",
        "endDate":"2018-04-28 23:59:52","token": "zwoqgqod-c392-ingy-6cyl-stvk7nadyrpe"
    }
    :return: json
    """
    # 公告标题 状态 开始时间 结束时间
    conditions = request.get_json()
    type = conditions.get("type")
    status = conditions.get("status")
    end_date = conditions.get("endDate")  # 结束时间
    start_date = conditions.get("startDate")  # 开始时间

    # 开始构造查询语句，分别根据参数是否为空来构造sql语句
    conditions_sql = "select a.*, b.path as imgPath from tbl_carouse" \
                     " as a JOIN tbl_image_sources as b where a.imgId=b.id "
    if _admin_parameters_filter([type]):
        conditions_sql += "and a.type=%d " % type
    if _admin_parameters_filter([status]):
        conditions_sql += "and a.status=%d " % status

    # 创建公告的开始和结束时间
    if _admin_parameters_filter([start_date]):
        if _admin_parameters_filter([end_date]):
            conditions_sql += "and a.createDate > '%s' and a.createDate < '%s'" % (start_date, end_date)
        else:
            conditions_sql += "and a.createDate > '%s'" % start_date
    else:
        if _admin_parameters_filter([end_date]):
            conditions_sql += "and a.createDate < '%s'" % end_date

    datas = {"carouses": query(conditions_sql)}
    return json(get_json(data=datas))



@bp.route("/addCarouse/", methods=["POST"])
@_admin_permission_required
def add_carouse():
    """
    增加轮播图
    :arg {"type":0, "imgId":1,"status":1,"content":"", "url":"http://www.google.com/", "token": "zwoqgqod-c392-ingy-6cyl-stvk7nadyrpe"}
    :arg {"type":1, "imgId":1,"status":1,"content":"123", "url":"","token": "zwoqgqod-c392-ingy-6cyl-stvk7nadyrpe"}
    :return: json
    """
    carouse_info = request.get_json()
    url = carouse_info.get("url")
    type = carouse_info.get("type")
    img_id = carouse_info.get("imgId")
    status = carouse_info.get("status")
    content = carouse_info.get("content")
    create_date = get_current_time()

    # 参数校验,如果type为0，url不能为空；如果如果为1，content不能为空
    if type!=None and type == 0:
        paras = [type, img_id, status, url]
    else:
        paras = [type, img_id, status, content]
    if not _admin_parameters_filter(paras):
        return json(get_json(code=-200, msg="操作失败，参数有误!"))

    # 构造sql并执行
    insert_anno_sql = "INSERT into tbl_carouse " \
                      "values(NULL, %d, %d, %d, '%s', '%s', '%s')" % (type, img_id, status, content, url, create_date)
    if excute(insert_anno_sql):
        return json(get_json(msg="添加成功!"))

    return json(get_json(code=-100, msg="添加失败，请检查数据库链接!"))


@bp.route("/updateCarouse/", methods=["POST"])
@_admin_permission_required
def update_carouse():
    """
    修改轮播图
    :arg {"id":1, "type":0, "imgId":1,"status":1,"content":"", "url":"http://www.google.com/","token": "zwoqgqod-c392-ingy-6cyl-stvk7nadyrpe"}
    :arg {"id":1, "type":1, "imgId":1,"status":1,"content":"123", "url":"","token": "zwoqgqod-c392-ingy-6cyl-stvk7nadyrpe"}
    :return:
    """
    carouse_info = request.get_json()
    id = carouse_info.get("id")
    url = carouse_info.get("url")
    type = carouse_info.get("type")
    img_id = carouse_info.get("imgId")
    status = carouse_info.get("status")
    content = carouse_info.get("content")

    # 参数校验,如果type为0，url不能为空；如果如果为1，content不能为空
    if type!=None and type == 0:
        paras = [type, img_id, status, url]
    else:
        paras = [type, img_id, status, content]
    if not _admin_parameters_filter(paras):
        return json(get_json(code=-200, msg="操作失败，参数有误!"))

    # 更新轮播图信息
    update_carouse_sql = "update tbl_carouse set type=%d, imgId=%d, status=%d, content='%s', url='%s' where id=%d" % \
                         (type, img_id, status, content, url, id)
    if excute(update_carouse_sql):
        return json(get_json())

    return json(get_json(code=-100, msg="添加失败，请检查数据库链接!"))


@bp.route("/deleteCarouse/", methods=["POST"])
@_admin_permission_required
def delete_carouse():
    """
    删除轮播图
    :arg {"id":1, "token": "zwoqgqod-c392-ingy-6cyl-stvk7nadyrpe"}
    :return:
    """
    carouse_info = request.get_json()
    id = carouse_info.get("id")

    # 参数校验
    if not _admin_parameters_filter([id]):
        return json(get_json(code=-200, msg="操作失败，参数有误!"))

    # 更新轮播图
    update_carouse_sql = "update tbl_carouse set status=0 where id=%d" % id
    if excute(update_carouse_sql):
        return json(get_json())

    return json(get_json(code=-100, msg="添加失败，请检查数据库链接!"))