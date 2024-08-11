from src import app, login_manager
from src.cctv.controllers.controller import handle_login, handle_registration , handle_add_zone , handle_retrieves_zone , handle_add_camera , handle_retrieves_camera , user_list
from src.cctv.models.model import Users, db , Camera
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
    

@app.route('/users')
def list_users():
    return jsonify(user_list()), 200


@app.route('/api/add-zone' , methods=['POST'])
def api_add_zone():
    if request.method == 'POST':
        zone_name = request.json['zone_name']
        zone_desc = request.json['zone_desc']
        success , message = handle_add_zone(zone_name , zone_desc)

        if success:
            return jsonify(message=message , success=success)
        else:
            return jsonify(message=message , success=success)
    else:
        return jsonify(message= 'ivailde request') , 405
    

@app.route('/api/zones')
def api_zones():
    zones = handle_retrieves_zone()    
    return jsonify(zones = zones)

@app.route('/api/add-camera', methods=['POST' ])
def api_add_camera():
    if request.method == 'POST':
        data = request.json
        camera_name = data.get('camera_name')
        camera_ip = data.get('camera_ip')
        camera_username = data.get('camera_username')
        camera_password = data.get('camera_password')
        camera_type = data.get('camera_type')
        zone_name = data.get('zone')

        success, message = handle_add_camera(camera_ip, camera_name, camera_username, camera_type, camera_password, zone_name)

        return jsonify(message=message, success=success)
    else:
        return jsonify(message='Invalid request'), 405

@app.route('/api/cameras')
def api_cameras():
    cameras = handle_retrieves_camera()
    return jsonify(cameras = cameras)