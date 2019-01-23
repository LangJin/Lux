# -*- coding:utf-8 -*-
__author__ = 'snake'
from app import create_app
from app.resources import users, admin


app = create_app("ProductionConfig")

if __name__ == "__main__":
    app.run()
