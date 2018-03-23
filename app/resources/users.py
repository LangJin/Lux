from app import bp
from app.common import util_db as db
from app.common.util_json import get_json
from flask import jsonify, request, redirect, url_for, session
from app.common.util_db import query

def _is_logined():
    """判断用户是否登录
    """

    if session.get("user"):
        return True
    return False



@ bp.route("/")
def index():
    """首页接口
    """

    datas = {}          # 数据集合
    articles = []       # 文章处理
    # 查询用户信息
    datas["user"] = []
    if _is_logined():
        query_user_sql = "select * from tbl_user where id = %s" % session.get("user")
        datas["user"] = query(query_user_sql)

    # 查询文章信息
    for type in range(1,6):
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

    return jsonify(get_json(data=datas))



@bp.route("/userLogin/", methods=["POST"])
def user_login():
    """
        用户登录
        :arg user, password, captcha
        :return json
    """

    return jsonify(get_json(url="/"))




