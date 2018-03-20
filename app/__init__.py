# -*- coding:utf-8 -*-
__author__ = 'lux'


from flask import Flask, Blueprint
from config import config



bp = Blueprint("bp", __name__ )

def create_app(config_name="DevelopConfig"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # 注册蓝本
    app.register_blueprint(bp)

    return app