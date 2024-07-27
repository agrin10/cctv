from src import app
from src.cctv.controllers.controller import registeration , log_in
from src.cctv.models.model import Users
from flask import render_template, request, redirect, url_for, flash , jsonify
from src.cctv.models.model import Users, db
from flask_login import login_user , logout_user , login_required 
from src import app




@app.route('/register' , methods=['POST' , 'GET'])
def registration():
    if request.method == 'POST':
        if request.is_json:
            username = request.form['username']
            password = request.form['password']
            existing_user = Users.query.filter_by(username=username)
            if existing_user == username:
                return jsonify(message="user already exist")
                
        
            new_user = Users(username= username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            db.session.rollback()
            return jsonify(message="registeration successfuly. please log in ")
        return render_template('register.html')
@app.route('/login' , methods=['POST' , 'GET'])
def log_in():
    if request.method == 'POST':
        if request.is_json:
            Username = request.form['username']
            password = request.form['password']

            user = Users.query.filter_by(username = Username).first()
            if user is None:
                return jsonify(message='Username does not exist')

            if user and user.check_password(password):
                login_user(user)
                return jsonify(message='loged in successfuly')

            else: 
                return jsonify(message='invaild password and username')
            
    return render_template('login.html')





