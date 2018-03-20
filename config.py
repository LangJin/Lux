# -*- coding:utf-8 -*-
__author__ = 'lux'

import os

# 开发环境
class DevelopConfig:
    # FLASK启动配置
    DEBUG = True
    HOST = "0.0.0.0"
    SECRET_KEY = os.urandom(24)    # SESSION配置


# 线上发布环境
class DeployConfig:
    # FLASK启动配置
    DEBUG = True
    HOST = "0.0.0.0"
    SECRET_KEY = os.urandom(24)    # SESSION配置



config = {
    "DevelopConfig": DevelopConfig,
    "DeployConfig" : DeployConfig
}

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'db': 'lux',
    'charset': 'utf8mb4'
}