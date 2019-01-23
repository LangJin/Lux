# -*- coding:utf-8 -*-
__author__ = 'snake'

import os



DevelopConfig = {
    "DEBUG": True,
    "HOST": "0.0.0.0",
    "JSON_AS_ASCII": False,  # json 中文支持
    "BABEL_DEFAULT_LOCALE": "zh",
    "SECRET_KEY": os.urandom(24),  # SESSION配置
    "THREADED": True
}

ProductionConfig = {
    "DEBUG": False,
    "HOST": "0.0.0.0",
    "JSON_AS_ASCII": False,  # json 中文支持
    "BABEL_DEFAULT_LOCALE": "zh",
    "SECRET_KEY": os.urandom(24),  # SESSION配置
    "THREADED":True
}

FlaskConfig = {
    "DevelopConfig": DevelopConfig,
    "ProductionConfig": ProductionConfig
}

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'db': 'lux',
    'charset': 'utf8mb4'
}

upload_config = {
    "UPLOAD_FOLDER":"C:\\Users\\SNake\\PycharmProjects\\Lux\\app\\static\\uploads"
}
