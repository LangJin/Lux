from app import bp
from functools import wraps
from app.common import util_db as db
from app.common.util_json import get_json
from flask import jsonify as json, request, redirect, url_for, session
from app.common.util_db import query, excute
from app.common.util_date import get_current_time


def _is_logined():
    """
    判断用户是否登录
    """
    if session.get("user"):
        return True
    return False


def _permission_required(func):
    """
    登陆装饰器
    :param func:
    :return: json
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("user"):
            return func(*args, **kwargs)
        return json(get_json(code=-300, msg="login first please!", url="/"))

    return wrapper


@bp.route("/")
def index():
    """
    首页接口
    :arg
    :return json
    """
    datas = {}  # 返回的数据集，包括用户信息、文章分类和信息、跑马灯、轮播图
    datas["user"] = [] # 用户信息默认值
    if _is_logined():
        datas["user_info"] = session.get("user")

    # 查询文章信息
    articles = []
    for type in range(1, 6):
        title = "article" + str(type)
        query_article_sql = "select * from tbl_article where type=%s LIMIT 1,10" % str(type)
        articles.append({title: query(query_article_sql)})
    datas["articles"] = articles

    # 查询跑马灯信息
    query_anno_sql = "select * from tbl_announcement LIMIT 1,10"
    datas["annos"] = query(query_anno_sql)

    # 查询轮播图信息
    datas["carouses"] = []
    # todo
    # 没有轮播图怎么查？

    return json(get_json(data=datas))


@bp.route("/userLogin/", methods=["POST"])
def user_login():
    """
    用户登录
    :arg {"username":"user", "password":"123", "capcha":"123456"}
    :return json
    """
    user_info = request.get_json()
    captcha = user_info.get("captcha")
    username = user_info.get("username")
    password = user_info.get("password")
    # todo
    # 修改验证码
    if captcha == "123456":
        query_login_sql = "select * from tbl_user where username='%s' and password='%s'" % (username, password)
        result = query(query_login_sql)
        if result:
            session["user"] = result
            return json(get_json(url="/"))

    return json(get_json(code="-100", msg="login failed", url=""))


@bp.route("/userRegist/", methods=["POST"])
def user_regist():
    """
    用户注册
    :arg {"username":"user", "password":"123", "nickname":"nickname"}
    :return json
    """
    user_info = request.get_json()
    nickname = user_info.get("nickname")
    username = user_info.get("username")
    password = user_info.get("password")
    create_date = get_current_time()

    user_reg_sql = "insert into tbl_user values(NULL, '%s', '%s', '%s',1,'','','',NULL,'','','','','','','%s',NULL)" % (
                    username, password, nickname, create_date)
    if excute(user_reg_sql) == 1:
        return json(get_json(url="/loginPage.html"))

    return json(get_json(code=-100, msg="regist falied" ,url=""))


@bp.route("/userLogout/")
@_permission_required
def user_logout():
    """
    用户退出，删除session
    :return:
    """
    session.pop("user", None)
    return json(get_json(url="/"))


"""用户登陆后有个人中心，能够看到自己的历史评论、收藏的文章、浏览的记录，以及自己的个人资料的编辑。"""
@bp.route("/userIndex/")
@_permission_required
def user_index():
    """
    获取用户个人中心信息,包括历史评论、收藏文章、浏览记录、个人资料
    :return:
    """
    datas = {}
    user = session.get("user")
    # 历史评论 {}
    # todo 还没有想好文章和评论一对多的关系如何表示 哎
    query_comment_his_sql = ""
    datas["comments"] = []

    # 收藏文章
    query_collect_sql = "select a.* from tbl_article as a RIGHT JOIN tbl_article_collect as b on a.id=b.articleId and b.userId=%s" % user[0][0]
    datas["collects"] = query(query_collect_sql)

    # 浏览记录
    query_browsing_his_sql = "select a.* from tbl_article as a RIGHT JOIN tbl_article_browsing_history as b on a.id=b.articleId and b.userId=%s" % user[0][0]
    datas["browsing"] = query(query_browsing_his_sql)

    # 个人喜欢
    query_like_sql = "select a.* from tbl_article as a RIGHT JOIN tbl_article_like as b on a.id=b.articleId and b.userId=%s" % user[0][0]
    datas["likes"] = query(query_like_sql)

    # 个人资料
    datas["user_info"] = user

    return json(get_json(data=datas))