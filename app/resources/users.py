from app import bp
from app.common import util_db as db
from app.common.util_json import get_json
from flask import jsonify as json, request, redirect, url_for, session
from app.common.util_db import query, excute
from app.common.util_date import get_current_time


def _is_logined():
    """判断用户是否登录
    """

    if session.get("user"):
        return True
    return False



@bp.route("/")
def index():
    """ 首页接口
        :arg
        :return json
    """

    datas = {}  # 数据集合
    # 查询用户信息
    datas["user"] = []
    if _is_logined():
        datas["user"] = session.get("user")

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
        :arg username, password, captcha
        :return json
    """

    captcha = request.form.get("captcha")
    username = request.form.get("username")
    password = request.form.get("password")
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
        :arg username, password, captcha
        :return json
    """

    nickname = request.form.get("nickname")
    username = request.form.get("username")
    password = request.form.get("password")
    createDate = get_current_time()

    user_reg_sql = "insert into tbl_user values(NULL, '%s', '%s', '%s',1,'','','',NULL,'','','','','','','%s',NULL)" % (
                    username, password, nickname, createDate)
    if excute(user_reg_sql) == 1:
        return json(get_json(url="/loginPage.html"))
    return json(get_json(code=-100, msg="regist falied" ,url=""))