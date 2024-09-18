from flask import redirect , url_for , render_template , request , flash 
import os
from flask_jwt_extended import  jwt_required  
from src.setting import setting_bp



@setting_bp.route('/')
def setting():
    return render_template('setting.html')

@setting_bp.route('/user')
def user_mange():
    return render_template('user-manage.html')