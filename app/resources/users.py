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
    datas["user"] = []  # 用户信息默认值
    if _is_logined():
        datas["user_info"] = session.get("user")

    # 查询文章信息
    articles = []
    for type in range(1, 6):
        title = "article" + str(type)
        query_article_sql = "select * from tbl_article where type=%s LIMIT 10" % str(type)
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

    # 判断用户名是否已被占用
    query_user_sql = "select * from tbl_user where username='%s'" % username
    if query(query_user_sql):
        return json(get_json(code=-300, msg="username is exsits!"))

    # 没被占用，进行注册
    user_reg_sql = "insert into tbl_user values(NULL, '%s', '%s', '%s',1,'','','',NULL,'','','','','','','%s',NULL)" % (
        username, password, nickname, create_date)
    if excute(user_reg_sql) == 1:
        return json(get_json(url="/loginPage.html"))

    return json(get_json(code=-100, msg="regist falied", url=""))


@bp.route("/userLogout/")
@_permission_required
def user_logout():
    """
    用户退出，删除session
    :return:
    """
    session.pop("user", None)
    return json(get_json(url="/"))


@bp.route("/userIndex/")
@_permission_required
def user_index():
    """
    获取用户个人中心信息,包括历史评论、收藏文章、浏览记录、个人资料
    :return: json
    """
    datas = {}
    user = session.get("user")
    # 历史评论 格式：[{"article": (), "comment": ()}]
    article_comments = {}
    query_comment_his_sql = "select * from tbl_article_comment where userId='%s' ans status=1 LIMIT 10" % user[0][0]
    for comment in query(query_comment_his_sql):
        article_id = comment[2]
        query_article_comment_sql = "select * from tbl_article where id='%s' and status=1" % article_id  # 默认文章1状态为有效
        article_comments.append({"article": query(query_article_comment_sql), "comment": comment})
    datas["comments"] = article_comments

    # 收藏文章
    query_collect_sql = "select a.* from tbl_article as a RIGHT JOIN tbl_article_collect as b on a.id=b.articleId and b.userId=%s" % \
                        user[0][0]
    datas["collects"] = query(query_collect_sql)

    # 浏览记录
    query_browsing_his_sql = "select a.* from tbl_article as a RIGHT JOIN tbl_article_browsing_history as b on a.id=b.articleId and b.userId=%s" % \
                             user[0][0]
    datas["browsing"] = query(query_browsing_his_sql)

    # 个人喜欢
    query_like_sql = "select a.* from tbl_article as a RIGHT JOIN tbl_article_like as b on a.id=b.articleId and b.userId=%s" % \
                     user[0][0]
    datas["likes"] = query(query_like_sql)

    # 个人资料
    datas["user_info"] = user

    return json(get_json(data=datas))


@bp.route("/userInfoPage/")
@_permission_required
def user_info_page():
    """
    进入页面时请求此接口
    :return: json
    """
    return json(get_json(data=session.get("user")))


@bp.route("/updateUserInfo/", methods=["POST"])
@_permission_required
def update_user_info():
    """
    编辑用户信息
    :arg {"sex":"男", "age":22, "email":"test@qq.com", "wechat":"snake", "remark":"greate full!", "address":"test", "nickname":"snake", "signature":"signature", "cellphone":"15000000000", "education":"education"}
    :return: json
    """
    user_info = request.get_json()
    sex = user_info.get("sex")
    age = int(user_info.get("age"))
    email = user_info.get("email")
    wechat = user_info.get("wechat")
    remark = user_info.get("remark")
    address = user_info.get("address")
    nickname = user_info.get("nickname")
    signature = user_info.get("signature")
    cellphone = user_info.get("cellphone")
    education = user_info.get("education")
    updateDate = get_current_time()

    # 执行用户信息更新
    update_user_sql = "update tbl_user set nickname='%s',sex='%s',age=%d, email='%s', wechat='%s',remark='%s',address='%s',nickname='%s',signature='%s',cellphone='%s',education='%s',updateDate='%s' where id='%s'" % (
        nickname, sex, age, email, wechat, remark, address, nickname, signature, cellphone, education, updateDate,
        session.get("user")[0][0])

    print(update_user_sql)
    return json(get_json(data=session.get("user")))

# todo
# 头像上传和修改，如果实现接口公用还没想好，哎
