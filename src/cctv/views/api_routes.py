from src import app
from src.cctv.controllers.controller import handle_login, handle_registration , handle_add_zone , handle_retrieves_zone , handle_add_camera , handle_retrieves_camera, handle_logout , get_records_from_api , get_alerts_from_api

from flask import request, jsonify 
from flask_login import login_user , logout_user
from flask_jwt_extended import jwt_required


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

@app.route('/api/login', methods=['POST'])
def api_login():
    username = request.json['username']
    password = request.json['password']
    user, success, message,  response = handle_login(username, password)
    if success:
        login_user(user)
        return response
    else:
        return jsonify(message=message, success=success), 401




    
@app.route('/api/logout', methods=['POST'])
@jwt_required()
def api_logout():
    logout_user()
    response = handle_logout()
    return response

@app.route('/api/add-zone' , methods=['POST'])
@jwt_required()
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
@jwt_required()
def api_zones():
    zones = handle_retrieves_zone()    
    return jsonify(zones = zones)

@app.route('/api/add-camera', methods=['POST' ])
@jwt_required()
def api_add_camera():
    if request.method == 'POST':
        data = request.json
        camera_name = data.get('camera_name')
        camera_ip = data.get('camera_ip')
        camera_username = data.get('camera_username')
        camera_password = data.get('camera_password')
        camera_type = data.get('camera_type')
        zone_name = data.get('zone')
        camera_image= None

        success, message = handle_add_camera(camera_ip, camera_name, camera_username, camera_type, camera_password, zone_name, camera_image)

        return jsonify(message=message, success=success)
    else:
        return jsonify(message='Invalid request'), 405

@app.route('/api/cameras')
@jwt_required()
def api_cameras():
    cameras = handle_retrieves_camera()
    return jsonify(cameras = cameras)


@app.route('/api/alerts')
def api_alerts():
    data = get_alerts_from_api()
    return jsonify(data)

@app.route('/api/search-files')
def search_files():
    start_time = request.args.get('from')
    end_time = request.args.get('to')
    
    data = get_records_from_api(start_time , end_time)
    return jsonify(data=data)

# @app.route('/api/get-devices')
# def get_devices():
#     data = api_get_devices()
#     return jsonify(data)

