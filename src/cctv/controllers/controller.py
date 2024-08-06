from flask import render_template, request, redirect, url_for, flash , jsonify
from src.cctv.models.model import Users, db
from flask_login import login_user , logout_user , login_required , current_user
from src import login_manager

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)



def handle_registration(username , password , email):
    
    existing_user = Users.query.filter_by(username = username).first()
    if existing_user:
        return False , 'username already exists' 
    if password is None:
        return False , 'password is required' 
    new_user = Users(username = username , email = email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    return True , 'registration successful, please login'         
        

def handle_login(username , password):
    user = Users.query.filter_by(username = username).first()
    if user is None:
        return user , False , 'username not found' 
    if user.check_password(password):
        return user ,  True , 'login successfully' 
    return user,  False,'invalid password' 


    






