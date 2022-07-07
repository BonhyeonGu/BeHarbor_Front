from flask import Blueprint, render_template, request, session, jsonify
import pymysql

login_back = Blueprint('login_back', __name__, template_folder='templates')
@login_back.route('/<page>')
def login_back():
    
