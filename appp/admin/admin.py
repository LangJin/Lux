# coding:utf-8

#admin.py

from flask import Blueprint,render_template, request

admin = Blueprint('admin',__name__)

 
@admin.route('/add')
def add():
    return 'admin_add'

@admin.route('/show')
def show():
    return 'admin_show'