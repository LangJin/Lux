# -*- coding:utf-8 -*-
__author__ = 'lux'
from app import create_app


app = create_app("DevelopConfig")

if __name__ == "__main__":
    app.run()
