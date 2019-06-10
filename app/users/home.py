from flask import jsonify
from . import userbp



@userbp.route("/title")
def title():
    data = {
        "username":"张三"
    }
    return jsonify(data)


@userbp.route("/")
def index():
    return "<h1>你好</h1>"