from src import app
from flask import render_template, request, redirect, url_for, flash
from src.cctv.controllers.controller import handle_registration, handle_login
from flask_login import login_user, logout_user, login_required 

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        success, message = handle_registration(username, password, email)
        flash(message=message)
        if success:
            return redirect(url_for('login'))
        else:
            return redirect(url_for('register'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user, success, message = handle_login(username, password) 
        if success:
            login_user(user)
            flash(message=message)  
            return redirect(url_for('index'))
        else:
            flash(message=message)  
            return redirect(url_for('register')) 
    return render_template('login.html')

@app.route('/camera-list' , methods=['POST' , 'GET'])
def camera_list():
    return render_template('list-cam.html')


@app.route('/add-camera' , methods=['POST' , 'GET'])
def add_camera():
    return render_template('add-cam.html')



@app.route('/zone-list' , methods=['POST' , 'GET'])
def zone_list():
    return render_template('zone-list.html')


@app.route('/add-zone' , methods=['POST' , 'GET'])
def add_zone():
    return render_template('add-zone.html')

