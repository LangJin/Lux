# -*- coding:utf-8 -*-
__author__ = 'lux'


from api import index
from api import create_app


app = create_app("DevelopConfig")

if __name__ == "__main__":
    app.run()