# -*- coding:utf-8 -*-
__author__ = 'LangJin'
from config import config
from flask import Flask, Blueprint

bp = Blueprint("bp", __name__)


def create_app(config_name="Develop"):
    app = Flask(__name__)
    app.config.update(config[config_name])
    app.register_blueprint(bp)  # 注册蓝本

    return app
