from src import app, login_manager
from src.cctv.controllers.controller import handle_login, handle_registration
from src.cctv.models.model import Users, db
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required 

@app.route('/api/register', methods=['POST', 'GET'])
def api_register():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
        success, message = handle_registration(username, password, email)
        return jsonify(message=message, success=success)
    else:
        return jsonify({'message': 'Registration Failed'}), 400 

@app.route('/api/login', methods=['POST', 'GET'])
def api_login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        user, success, message = handle_login(username, password)  
        if success:
            login_user(user)
            return jsonify(message=message, success=success), 200
        else:
            return jsonify(message=message, success=success), 401
    else:
        return jsonify({'message': 'Login Failed'}), 400 