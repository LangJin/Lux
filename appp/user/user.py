#coding:utf-8

#user

from flask import Blueprint, render_template, redirect

user = Blueprint('user',__name__)

 
@user.route('/')
def index():
    return '嘻嘻'

@user.route('/add')
def add():
    return 'user_add'

@user.route('/show')
def show():
    return 'user_show'