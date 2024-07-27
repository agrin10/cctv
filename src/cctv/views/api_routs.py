from src import app
from src.cctv.controllers.controller import registeration , log_in
from src.cctv.models.model import Users
from flask import render_template, request, redirect, url_for, flash , jsonify
from src.cctv.models.model import Users, db
from flask_login import login_user , logout_user , login_required 
from src import app




@app.route('/register-api' , methods=['POST'])
def register_api():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            existing_user = Users.query.filter_by(username=username)
            if existing_user == username:
                return jsonify(message="user already exist")
            if not password:
                return jsonify(message="empty password")
        
            new_user = Users(username= username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify(message="registeration successfuly. please log in ")
    return jsonify(message="invalid request")

@app.route('/login-api' , methods=['POST'])
def login_api():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            Username = data.get('username')
            password = data.get('password')

            user = Users.query.filter_by(username = Username).first()
            if user is None:
                return jsonify(message='Username does not exist')

            if user and user.check_password(password):
                login_user(user)
                return jsonify(message='loged in successfuly')

            else: 
                return jsonify(message='invaild password and username')
            
    return jsonify(message="invalid request")





