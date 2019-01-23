# -*- coding:utf-8 -*-
__author__ = 'snake'
from config import FlaskConfig
from flask import Flask, Blueprint

bp = Blueprint("bp", __name__)


def create_app(config_name="ProductionConfig"):
    app = Flask(__name__)
    app.config.update(FlaskConfig[config_name])
    app.register_blueprint(bp)  # 注册蓝本

    return app
