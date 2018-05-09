# -*- conding:utf-8 -*-
__author__ = 'snake'

from app import bp
from functools import wraps
from app.utils.util_json import get_json
from flask import jsonify as json, request, session, render_template
from app.utils.util_db import query, excute
from app.utils.util_date import get_current_time
from app.utils.util_token import create_token
import os, config, traceback


def _is_logined():
    """
    判断用户是否登录
    """
    if session.get("user"):
        return True
    return False


def _set_user_session(user):
    """
    设置user的session，内容为user的数据库信息
    :param user: user数据库信息
    :return:
    """
    session.clear()
    session["user"] = user
    session["user_token"] = user.get("token")

def _get_user_session():
    """
    返回不包含password和token的user信息
    :return: {"userInfo":{}}
    """
    from copy import copy
    user = copy(session.get("user"))
    user.pop("token", None)
    user.pop("password", None)

    return {"userInfo": user}


def _user_permission_required(func):
    """
    登陆装饰器
    :param func:
    :return: json
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.get_json().get("token")
        if token is not None and token != ""\
                and token == session.get("user_token"):
            try:
                return func(*args, **kwargs)
            except:
                print(traceback.print_exc())
                return json(get_json(code=500, msg="内部错误,请检查参数是否正确!"))
        return json(get_json(code=-300, msg="权限错误,请先登录!"))

    return wrapper


def _upload_files(file, file_name):
    """
    上传图片公共方法
    :param file: 上传的file文件
    :return: True:成功;False失败
    """
    try:
        upload_path = os.path.join(config.upload_config.get("UPLOAD_FOLDER"), file_name)  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        file.save(upload_path)
        return True
    except:
        return False


def _parameters_filter(paras):
    """
    参数过滤，过滤条件为None或者""
    :param paras: []
    :return: False:不通过;True:通过
    """
    for para in paras:
        if para is None or para == "":
            return False
    return True


@bp.route("/")
def index():
    """
    首页接口
    :arg
    :return json
    """
    datas = {}  # 返回的数据集，包括用户信息、文章分类和信息、跑马灯、轮播图

    # 查询文章信息
    articles = []
    for type in range(1, 6):
        title = "article" + str(type)
        query_article_sql = "select * from tbl_article where type=%s LIMIT 10" % str(type)
        articles.append({title: query(query_article_sql)})
    # 查询跑马灯信息
    query_anno_sql = "select * from tbl_announcement where status=1 LIMIT 10"
    # 查询轮播图信息
    query_all_carouses_sql = "select a.*, b.path as imgPath " \
                             "from tbl_carouse as a JOIN tbl_image_sources as b " \
                             "where a.imgId=b.id and b.status=1 and a.status=1;"

    datas = {
        "articles": articles,
        "annos": query(query_anno_sql),
        "carouses": query(query_all_carouses_sql),
        "userInfo": session.get("user")
    }

    return json(get_json(data=datas))


@bp.route("/userLogin/", methods=["POST"])
def user_login():
    """
    用户登录
    :arg {"username":"user", "password":"123", "captcha":"123456"}
    :return json
    """
    user_info = request.get_json()
    captcha = user_info.get("captcha")
    username = user_info.get("username")
    password = user_info.get("password")

    # 参数校验
    if not _parameters_filter([username, password, captcha]):
        return json(get_json(code=-200, msg="参数存在空值，请检查参数!"))
    # todo
    # 修改验证码
    if captcha == "123456":
        query_login_sql = "select * from tbl_user where username='%s' and password='%s'" % (username, password)
        result = query(query_login_sql)
        if result:
            if result[0].get("status") == 1:
                # 生成并插入token
                user_token = create_token()
                insert_token_sql = "update tbl_user set token='%s' where id=%d" % (user_token, result[0]["id"])
                excute(insert_token_sql)

                # 查询IMG并更新Token
                query_img_sql = "select * from tbl_image_sources where id=%d" % result[0].get("imgId")
                result[0]["img"] = query(query_img_sql)[0].get("path")
                result[0]["token"] = user_token

                # 保存用户信息
                _set_user_session(result[0])
                return json(get_json(data={"token": user_token}, msg="登录成功!"))
            else:
                return json(get_json(msg="登录失败, 您已经禁止登陆网站, 请联系管理员处理!"))

    return json(get_json(code="-100", msg="登录失败，用户名或密码不正确!", ))


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

    # 参数校验
    if not _parameters_filter([username, password, nickname]):
        return json(get_json(code=-200, msg="参数存在空值，请检查参数!"))

    # 判断用户名是否已被占用
    query_user_sql = "select * from tbl_user where username='%s'" % username
    if query(query_user_sql):
        return json(get_json(code=-300, msg="用户名已存在!"))

    # 没被占用，进行注册
    user_reg_sql = "insert into tbl_user values(NULL, '%s', '%s', '%s'," \
                   "NULL, 1,'','','',NULL,'','','','',NULL,'','%s',NULL)" % (username, password, nickname, create_date)
    if excute(user_reg_sql):
        return json(get_json(msg="注册成功!"))

    return json(get_json(code=-100, msg="注册失败，用户名可能已经存在了!"))


@bp.route("/userLogout/", methods=["post"])
@_user_permission_required
def user_logout():
    """
    用户退出，删除session
    :arg {"token":"xxxxx"}
    :return:
    """
    session.pop("user", None)
    session.pop("user_token", None)
    return json(get_json())


@bp.route("/userIndex/", methods=["POST"])
@_user_permission_required
def user_index():
    """
    :params {"token":"pmqkp62j-n5pw-w882-zk3e-qh8722mivo4u"}
    获取用户个人中心信息,包括历史评论、收藏文章、浏览记录、个人资料
    :return: json
    """
    # 历史浏览
    user = _get_user_session()["userInfo"]
    query_comment_his_sql = "select * from tbl_article_comment as " \
                            "a join tbl_article as b where a.articleId=b.id " \
                            "and a.userId=%d and a.status=1 and b.status=1 limit 10" % user.get("id")
    # 收藏文章
    query_collect_sql = "select a.* from tbl_article as a JOIN " \
                        "tbl_article_collect as b on a.id=b.articleId " \
                        "and b.userId=%s and a.status=1 and b.status=1 " \
                        "limit 10" % user.get("id")
    # 浏览记录
    query_browsing_his_sql = "select a.* from tbl_article as a JOIN " \
                             "tbl_article_browsing_history as b on a.id=b.articleId " \
                             "and b.userId=%d and a.status=1 and b.status=1 limit 10" % user.get("id")
    # 个人喜欢
    query_like_sql = "select a.* from tbl_article as a JOIN " \
                     "tbl_article_like as b on a.id=b.articleId " \
                     "and b.userId=%d and a.status = 1 and b.status=1 limit 10" % user.get("id")

    # 构造响应数据
    datas = {
         "userInfo": _get_user_session().get("userInfo"),
         "likes": query(query_like_sql),
         "comments": query(query_comment_his_sql),
         "collects": query(query_collect_sql),
         "browsing": query(query_browsing_his_sql)
    }
    return json(get_json(data=datas))


@bp.route("/userInfoPage/", methods=["post"])
@_user_permission_required
def user_info_page():
    """
    进入页面时请求此接口
    :params {"token":"pmqkp62j-n5pw-w882-zk3e-qh8722mivo4u"}
    :return: json
    """
    return json(get_json(data=_get_user_session()))


@bp.route("/updateUserInfo/", methods=["POST"])
@_user_permission_required
def update_user_info():
    """
    编辑用户信息
    :arg {
        "sex":"男","imgId":1, "age":22, "email":"test@qq.com", "wechat":"snake", "remark":"greate full!",
        "address":"test", "nickname":"snake", "signature":"signature", "cellphone":"15000000000",
        "education":"education","token":"pmqkp62j-n5pw-w882-zk3e-qh8722mivo4u"
    }
    :return: json
    """
    user_info = request.get_json()
    sex = user_info.get("sex")
    age = user_info.get("age")
    token = user_info.get("token")
    email = user_info.get("email")
    img_id = user_info.get("imgId")
    wechat = user_info.get("wechat")
    remark = user_info.get("remark")
    address = user_info.get("address")
    nickname = user_info.get("nickname")
    signature = user_info.get("signature")
    cellphone = user_info.get("cellphone")
    education = user_info.get("education")
    updateDate = get_current_time()


    # 执行用户信息更新
    update_user_sql = "update tbl_user set nickname='%s', imgId=%d, sex='%s'," \
                      "age=%d, email='%s', wechat='%s',remark='%s',address='%s'," \
                      "nickname='%s',signature='%s',cellphone='%s',education='%s',updateDate='%s' where token='%s'" % \
                      (nickname, img_id, sex, age, email, wechat, remark, address, nickname, signature, cellphone,
                       education, updateDate, token)
    # 更新成功则重置session并返回最新的用户信息
    if excute(update_user_sql):
        user = query("select * from tbl_user where token='%s'" % token)[0]
        _set_user_session(user)

        # 返回用户信息
        return json(get_json(msg="修改成功", data=_get_user_session()))

    return json(get_json(code=-100, msg="修改失败!"))


@bp.route("/uploadPage/", methods=["GET"])
def upload_page():
    return render_template("uploadDemo.html")


@bp.route('/upload/', methods=['POST'])
def upload():
    """
    公共上传资源接口
    :arg file:上传文件格式;source:图片资源,详细请求数据参见uploadDemo.html
    :return:
    """
    # 检验来源
    file_source = request.form.get("source")
    if not _parameters_filter([file_source]):
        return json(get_json(code=-200, msg="参数存在空值，请检查参数!"))

    # 保存图片文件到服务器
    file = request.files['file']
    file_name = create_token() + "." + file.filename.split(".")[1]
    if _upload_files(file, file_name):
        # 执行插入数据库操作
        insert_img_source_sql = "INSERT INTO tbl_image_sources " \
                                "values(NULL, '%s', 1, '%s', NULL)" % (file_name, get_current_time())
        # 执行成功返回该img信息
        if excute(insert_img_source_sql):
            query_img_sql = "select * from tbl_image_sources where path='%s'" % file_name
            datas = {"imgInfo": query(query_img_sql)}
            return json(get_json(data=datas))

    return json(get_json(code=-100, msg="操作失败!"))


@bp.route("/articleDatiles/", methods=["POST"])
def article_detailes():
    """
    查询文章详情和评论
    :arg:   {"articleId":1}
    :return:
    """
    article_info = request.get_json()
    article_id = article_info.get("id")
    # id为空不允许
    if not _parameters_filter([article_id]):
        return json(get_json(code=-200, msg="参数存在空值，请检查参数!"))

    # -1：未登录用户
    user = session.get("user")
    if user:
        user_id = user.get("id")
    else:
        user_id = -1

    # 首先默认请求此接口为浏览了该文章
    try:
        # 增加浏览数量，如果没有浏览，则增加一条浏览数据，否则修改浏览时间
        query_article_sql = "select * from tbl_article_browsing_history " \
                            "as a where a.userId=%d and a.articleId=%d and a.status=1" % (user_id, article_id)
        if query(query_article_sql):
            article_browsing_sql = "update tbl_article_browsing_history set updateDate='%s'" % get_current_time()
            excute(article_browsing_sql)
        else:
            article_browsing_sql = "INSERT INTO tbl_article_browsing_history " \
                                   "VALUES (NULL, %d, %d, 1, '%s',NULL)" % (user_id, article_id, get_current_time())
            excute(article_browsing_sql)

        # 查询article阅读总数
        query_article_readcount_sql = "select * from tbl_article where id=%d" % article_id
        read_counts = query(query_article_readcount_sql)[0].get("readCount") + 1

        # 更新readCount总数
        update_article_browsing_count = "update tbl_article set readCount=%d, " \
                                        "updateDate='%s' where id=%d" % (read_counts, get_current_time(), article_id)
        excute(update_article_browsing_count)
    except Exception as e:
        print(e)
        pass

    # 查询文章和对应的评论
    query_article_sql = "select * from tbl_article where id=%s and status=1" % article_id
    query_comments_sql = "select * from tbl_article_comment where articleId=%s and status=1" % article_id
    results = {
        "article": query(query_article_sql),
        "comments": query(query_comments_sql)
    }

    return json(get_json(data=results))


@bp.route("/articleComment/", methods=["POST"])
@_user_permission_required
def article_comment():
    """
    文章评论
    :arg {"articleId":1, "content":"test", "token": "xx13v9wp-t4gl-gsxn-mnd6-ftnhx6gnp3r0"}
    :return: json
    """
    comments_info = request.get_json()
    user_id = session.get("user").get("id")
    article_id = comments_info.get("id")
    comment_content = comments_info.get("content")
    # 参数校验
    if not _parameters_filter([article_id, comment_content]):
        return json(get_json(code=-200, msg="参数存在空值，请检查参数!"))

    # 增加文章评论
    insert_aritcle_comment_sql = "insert into tbl_article_comment values" \
                                 "(NULL, %d, %d, '%s', 1, '%s', NULL, NULL)" % \
                                 (user_id, article_id, comment_content, get_current_time())
    if excute(insert_aritcle_comment_sql):
        return json(get_json(msg="评论成功!"))

    return json(get_json(code=-100, msg="操作失败!"))


@bp.route("/replyComment/", methods=["POST"])
@_user_permission_required
def reply_comment():
    """
    回复评论
    :arg {"articleId":1, "commentId":5, "commentContent":"test","token": "xx13v9wp-t4gl-gsxn-mnd6-ftnhx6gnp3r0"}
    :return: json
    """
    comments_info = request.get_json()
    article_id = comments_info.get("articleId")
    comment_id = comments_info.get("commentId")
    comment_content = comments_info.get("commentContent")
    # 参数校验
    if not _parameters_filter([article_id, comment_id, comment_content]):
        return json(get_json(code=-200, msg="参数存在空值，请检查参数!"))

    # 文章下是否有此评论，这里有bug todo

    # 增加文章评论
    user_id = session.get("user").get("id")
    insert_reply_comment_sql = "insert into tbl_article_comment values" \
                               "(NULL, %d, %d, '%s', 1, '%s', NULL, %d)" % \
                               (user_id, article_id, comment_content, get_current_time(), comment_id)
    if excute(insert_reply_comment_sql):
        return json(get_json())

    return json(get_json(code=-100, msg="操作失败，请检查数据库链接!"))


@bp.route("/articleCollect/", methods=["POST"])
@_user_permission_required
def article_collect():
    """
    收藏文章
    :arg {"articleId":1,"token": "xx13v9wp-t4gl-gsxn-mnd6-ftnhx6gnp3r0"}
    :return: json
    """
    article_info = request.get_json()
    article_id = article_info.get("articleId")
    # 参数校验
    if not _parameters_filter([article_id]):
        return json(get_json(code=-200, msg="参数存在空值，请检查参数!"))

    # 检查是否已经收藏过文章
    user_id = session.get("user").get("id")
    query_article_collect_detail = "select * from tbl_article_collect as a " \
                                   "where a.userId=%d and a.articleId=%d and a.status=1" % (user_id, article_id)
    if query(query_article_collect_detail):
        return json(get_json(code=-100, msg="您已经收藏过此文章了!"))

    # 检查是否存在文章
    query_article_sql = "select * from tbl_article where id=%d and status=1" % article_id
    if not query(query_article_sql):
        return json(get_json(code=-100, msg="文章不在了...!"))

    # 增加文章收藏记录
    insert_article_collect_sql = "insert into tbl_article_collect " \
                                 "values(NULL, %d, %d, 1, '%s', NULL )" % (user_id, article_id, get_current_time())
    if excute(insert_article_collect_sql):
        return json(get_json(msg="收藏文章成功!"))

    return json(get_json(code=-100, msg="操作失败，请检查数据库链接!"))


@bp.route("/articleLike/", methods=["POST"])
@_user_permission_required
def article_like():
    """
    文章点赞
    :arg {"articleId":1,"token": "xx13v9wp-t4gl-gsxn-mnd6-ftnhx6gnp3r0"}
    :return: json
    """
    article_info = request.get_json()
    article_id = article_info.get("articleId")
    # 参数校验
    if not _parameters_filter([article_id]):
        return json(get_json(code=-200, msg="参数存在空值，请检查参数!"))

    # 检查是否已经赞过了
    user_id = session.get("user").get("id")
    query_article_like_detail = "select * from tbl_article_like as a  " \
                                "where a.userId=%d and a.articleId=%d and a.status=1" % (user_id, article_id)
    if query(query_article_like_detail):
        return json(get_json(code=-100, msg="您已经赞过了此文章!"))

    # 检查是否存在文章
    query_article_sql = "select * from tbl_article as a where a.id=%d and a.status=1" % article_id
    if not query(query_article_sql):
        return json(get_json(code=-100, msg="文章不在了...!"))

    # 如果存在记录则修改时间，如果没有记录则增加记录
    query_article_like_detail = "select * from tbl_article_like as a  where " \
                                "a.userId=%d and a.articleId=%d" % (user_id, article_id)
    if query(query_article_like_detail):
        update_article_collect_sql = "update tbl_article_like as a " \
                                     "set a.status=1 where a.userId=%d and a.articleId=%d" % (user_id, article_id)
    else:
        update_article_collect_sql = "insert into tbl_article_like " \
                                     "values(NULL, %d, %d, 1, '%s', NULL )" % (user_id, article_id, get_current_time())
    if excute(update_article_collect_sql):
        return json(get_json(msg="文章点赞成功!"))

    return json(get_json(code=-100, msg="操作失败，请检查数据库链接!"))


@bp.route("/cancelArticleCollent/", methods=["POST"])
@_user_permission_required
def cancel_article_collent():
    """
    取消文章关注
    :arg {"articleId":1,"token": "xx13v9wp-t4gl-gsxn-mnd6-ftnhx6gnp3r0"}
    :return:
    """
    article_info = request.get_json()
    article_id = article_info.get("articleId")
    # 参数校验
    if not _parameters_filter([article_id]):
        return json(get_json(code=-200, msg="参数存在空值，请检查参数!"))

    # 检查是否已经收藏过了
    user_id = session.get("user").get("id")
    query_article_collect_detail = "select * from tbl_article_collect as a " \
                                   "where a.userId=%d and a.articleId=%d and a.status=1" % (user_id, article_id)
    if not query(query_article_collect_detail):
        return json(get_json(code=-100, msg="您还没有收藏此文章!"))

    # 修改状态，如果存在记录就修改，没有就增加
    query_article_like_detail = "select * from tbl_article_collect as a" \
                                " where a.userId=%d and a.articleId=%d" % (user_id, article_id)
    if query(query_article_like_detail):
        update_article_collect_sql = "update tbl_article_collect as a set a.status=1 " \
                                     "where a.userId=%d and a.articleId=%d" % (user_id, article_id)
    else:
        update_article_collect_sql = "update tbl_article_collect as a set a.status=0 " \
                                     "where userId=%d and articleId=%d" % (user_id, article_id)
    if excute(update_article_collect_sql):
        return json(get_json(msg="成功取消收藏此文章!"))

    return json(get_json(code=-100, msg="操作失败，请检查数据库链接!"))


@bp.route("/cancelArticleLike/", methods=["POST"])
@_user_permission_required
def cancel_article_like():
    """
    取消文章点赞
    :arg {"articleId":1,"token": "xx13v9wp-t4gl-gsxn-mnd6-ftnhx6gnp3r0"}
    :return:
    """
    article_info = request.get_json()
    article_id = article_info.get("articleId")
    # 参数校验
    if not _parameters_filter([article_id]):
        return json(get_json(code=-200, msg="参数存在空值，请检查参数!"))

    # 检查是否已经赞过了
    user_id = session.get("user").get("id")
    query_article_like_detail = "select * from tbl_article_like as a " \
                                "where a.userId=%d and a.articleId=%d and a.status=1" % (user_id, article_id)
    if not query(query_article_like_detail):
        return json(get_json(code=-100, msg="您还没有赞过此文章!"))

    # 修改状态
    update_article_like_sql = "update tbl_article_like as a set " \
                              "a.status=0 where a.userId=%d and a.articleId=%d" % (user_id, article_id)
    if excute(update_article_like_sql):
        return json(get_json(msg="成功取消此文章的点赞!"))

    return json(get_json(code=-100, msg="操作失败，请检查数据库链接!"))


@bp.route("/codeStatus/", methods=["post", "get"])
def get_code_status():
    datas = {"code:-100": "操作失败", "code:-200": "参数错误", "code:-300": "权限出错,需要登录", "code:200": "操作成功",
             "code:500": "内部异常，通常都是参数传错了"}
    return json(get_json(msg="状态码说明", data=datas))
