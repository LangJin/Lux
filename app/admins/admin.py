from flask import jsonify
from . import adminbp



@adminbp.route("/title")
def title():
    data = {
        "username":"张三"
    }
    return jsonify(data)


@adminbp.route("/")
def index():
    return "<h1>你好</h1>"