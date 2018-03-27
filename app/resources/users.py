from app import bp
from functools import wraps
from app.common import util_db as db
from app.common.util_json import get_json
from flask import jsonify as json, request, redirect, url_for, session, render_template
from app.common.util_db import query, excute
from app.common.util_date import get_current_time, create_token
import os, config


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


def _upload_files(file, file_name):
    """
    上传图片公共方法
    :param file: 上传的file文件
    :return: 1:成功;0失败
    """
    try:
        upload_path = os.path.join(config.upload_config.get("UPLOAD_FOLDER"), file_name)  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        file.save(upload_path)
        return 1
    except:
        return 0


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
            _set_user_session(result)
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
    return json(get_json(data=session.get("user"),url="/userInfoPage.html"))


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
    # 更新成功则重置session并返回最新的用户信息
    if excute(update_user_sql) == 1:
        _set_user_session(query("select * from tbl_user where id=%s" % session.get("user")[0][0]))
        return json(get_json(data=session.get("user")))

    return json(get_json(code=-100, msg="failed"))


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
    if file_source == "":
        return json(get_json(code=-200, msg="file source is null!"))

    # 如果上传成功，则进行更新对应的数据来源，如user头像
    file = request.files['file']
    file_name = create_token() + "." + file.filename.split(".")[1]
    if _upload_files(file, file_name) == 1:
        # 图片来源为用户头像，更新用户用户头像url
        if file_source == "userHeadImage":
            update_user_header_sql = "update tbl_user set headImage='%s' where id=%s" % (file_name, session.get("user")[0][0])
            if excute(update_user_header_sql) == 1: # 插入成功,就更新user信息
                _set_user_session(query("select * from tbl_user where id=%s"%session.get("user")[0][0]))
                return json(get_json(data=session.get("user")))

        # 文章header信息更新
        article_id = request.form.get("articleId")
        if file_source == "articleHeadImage" and article_id != None and article_id != "":
            update_article_header_sql = "update tbl_article set headImage='%s' where id=%s" % (file_name, article_id)
            if excute(update_article_header_sql) == 1:
                query_article_sql = "select * from tbl_article where id=%s" % article_id
                return json(get_json(data=query(query_article_sql)))

    return json(get_json(code=-100,msg="upload filed!"))


@bp.route("/articleDatiles/", methods=["POST"])
def article_detailes():
    """
    查询文章详情和评论
    :arg:   {"articleId":1}
    :return:
    """
    article_info = request.get_json()
    article_id = article_info.get("articleId")
    # id为空不允许
    if article_id == None or article_id == "":
        return json(get_json(code=-200, msg="article id is null!"))

    # -1：未登录用户
    if session.get("user"):
        user_id = session.get("user")[0][0]
    else:
        user_id = -1

    # 首先默认请求此接口为浏览了该文章
    try:
        # 增加浏览数量
        new_browsing_sql = "INSERT INTO tbl_article_browsing_history VALUES (NULL, %d, %d, 1, '%s',NULL)" % (user_id, article_id, get_current_time())
        excute(new_browsing_sql)

        # 查询article阅读总数
        query_article_readcount_sql = "select * from tbl_article_browsing_history where articleId=%s" % article_id
        read_counts = len(query(query_article_readcount_sql))

        # 更新readCount总数
        update_article_browsing_count = "update tbl_article set readCount=%d, updateDate='%s' where id=%s" % (read_counts, get_current_time(), article_id)
        excute(update_article_browsing_count)
    except Exception as e:
        print(e)
        pass

    # 查询文章和对应的评论
    query_article_sql = "select * from tbl_article where id=%s" % article_id
    query_comments_sql = "select * from tbl_article_comment where articleId=%s" % article_id
    results = {"article":query(query_article_sql), "comments":query(query_comments_sql)}

    return json(get_json(data=results))


@bp.route("/articleComment/", methods=["POST"])
@_permission_required
def article_comment():
    comments_info = request.get_json("comment")
    article_id = comments_info.get("articleId") # 文章id
    father_id = comments_info.get("fid") # 回复的评论id作为上级id
    content = comments_info.get("content")
    # todo 回复评论时应不应该添加article id？ 只是作为回复记录还是需要？？？  没想好  哎~~
    return json()

# todo
#  评论 收藏 点赞 各个页面入口接口 参数判断

