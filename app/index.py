# # -*- coding:utf-8 -*-
# __author__ = 'lux'
#
#
# from api import bp
# from common import util_db as db
# from common.util_json import get_json
# from flask import jsonify, request, redirect, url_for
#
#
# @bp.route("/", methods=["GET", "POST"])
# def index():
#     return jsonify(get_json(200, "OK", [], "/"))
#
#
# @bp.route("/test_get_method/", methods=["GET"])
# def test_get_method():
#     id = request.args.get("id")
#     return jsonify(get_json(code=200, msg="OK", data=[id], url="/"))
#
#
# @bp.route("/test_post_method/", methods=["POST"])
# def test_post_method():
#     id = request.form.get("id")
#     return jsonify(get_json(code=200, msg="OK", data=[id], url="/"))
#
#
# @bp.route("/test_db_query/")
# def test_db_query():
#     sql = "select * from tbl_test"
#     data = db.query(sql)
#     json = get_json(code=200, msg="OK", data=data, url="/")
#     return jsonify(json)
#
#
# @bp.route("/test_db_insert/")
# def test_db_insert():
#     name = "update_test_1"
#     sql = "update tbl_test set name='%s' where id=2" % name
#     db.excute(sql)
#
#     return redirect(url_for("bp.test_db_query"))  # 重定向到test_db_query接口
#
#
# @bp.route("/test_db_excutemany/")
# def test_db_excutemany():
#     name = "test_db_excutemany"
#     sql1 = "insert into tbl_test values(NULL,'%s')" % name
#     sql2 = "insert into tbl_test values(NULL,'%s')" % name
#     db.excutemany([sql1, sql2])
#
#     return redirect(url_for("bp.test_db_query"))  # 重定向到test_db_query接口
