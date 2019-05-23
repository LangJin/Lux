# coding:utf-8

from flask import Flask,request,render_template
from admin.admin import admin
from user.user import user

app=Flask(__name__)
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')


if __name__ == '__main__':
    app.run(debug=True)