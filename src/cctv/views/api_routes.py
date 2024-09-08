from app import app
from src.cctv.controllers.controller import handle_login, handle_registration , handle_add_zone , handle_retrieves_zone , handle_add_camera , handle_retrieves_camera, handle_logout , search_recorded_files , get_alerts_from_api , handle_edit_camera , handle_delete_camera , get_all_cameras_from_record_module, toggle_recording_camera , recording_status_specific_camera
from flask import request, jsonify  ,Blueprint
from flask_login import login_user , logout_user
from flask_jwt_extended import jwt_required

api_routes = Blueprint('api', __name__ , template_folder='templates' ,static_folder='static' )

@app.route('/api/register', methods=['POST'])
def api_register():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    success, message = handle_registration(username, password, email)
    return jsonify(message=message, success=success)
    
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
    zone_name = request.json['zone_name']
    zone_desc = request.json['zone_desc']
    success , message = handle_add_zone(zone_name , zone_desc)

    if success:
        return jsonify(message=message , success=success)
    else:
        return jsonify(message=message , success=success)

    

@app.route('/api/zones')
@jwt_required()
def api_zones():
    zones = handle_retrieves_zone()    
    return jsonify(zones = zones)

@app.route('/api/add-camera', methods=['POST' ])
@jwt_required()
def api_add_camera():
    data = request.json
    camera_name = data.get('camera_name')
    camera_ip = data.get('camera_ip')
    camera_username = data.get('camera_username')
    camera_password = data.get('camera_password')
    camera_type = data.get('camera_type')
    zone_name = data.get('zone')
    camera_port = data.get('port')
    camera_image= None
    recording =data.get('recording', False)
    ai_properties = data.get('ai_properties', [])



    success, message = handle_add_camera(camera_ip=camera_ip, camera_name=camera_name, camera_username=camera_username, camera_type=camera_type, camera_password=camera_password, zone_name=zone_name, camera_image=camera_image , recording=recording,ai_properties=ai_properties , camera_port=camera_port)

    return jsonify(message=message, success=success )


@app.route('/api/edit-camera', methods=['PATCH'])
def api_edit_camera():
    
    data = request.json

    camera_name = data.get('name')
    camera_ip = data.get('camera_ip')
    camera_new_ip = data.get('new_ip', camera_ip)  
    camera_new_name = data.get('new_name', camera_name)  
    camera_username = data.get('username')
    camera_new_username = data.get('new_username')
    camera_password = data.get('password')
    camera_new_password = data.get('new_password')
    camera_type = data.get('camera_type')
    camera_zone = data.get('new_zone')
    recording = data.get('recording', False)  
    ai_properties = data.get('ai_properties', [])  

    if not camera_name or not camera_ip:
        return jsonify({"success": False, "message": "Camera name and IP are required."}), 400

    success, message = handle_edit_camera(
        camera_ip=camera_ip,
        new_ip=camera_new_ip,
        name=camera_name,
        new_name=camera_new_name,
        username=camera_username,
        new_username=camera_new_username,
        password=camera_password,
        new_password=camera_new_password,
        camera_type=camera_type,
        camera_zone=camera_zone,
        recording=recording,
        ai_properties=ai_properties
    )

    if not success:
        return jsonify({"success": False, "message": message}), 400  
    return jsonify({"success": True, "message": message}), 200

@app.route('/api/delete-camera/<ip>-<name>' ,methods=['DELETE'])
def api_delete_camera(ip , name):
    status_code , success , message = handle_delete_camera(ip, name)
    if not success:
        return jsonify({"success": False, "message": message}), status_code
    return jsonify({"success": True, "message": message}), status_code
    

@app.route('/api/cameras')
@jwt_required()
def api_cameras():
    cameras = handle_retrieves_camera()
    return jsonify(cameras = cameras)


@app.route('/api/alerts')
@jwt_required()
def api_alerts():
    data = get_alerts_from_api()
    return jsonify(data)

@app.route('/api/search-files/<ip>-<name>')
@jwt_required()
def search_files(ip:str , name:str):
    start_time = request.args.get('from')
    end_time = request.args.get('to')
    data = search_recorded_files(camera_ip=ip , camera_name=name, from_=start_time , to_=end_time)
    return jsonify(data=data)


@app.route('/api/get-all-cameras-record-module')
def cameras_record():
    data = get_all_cameras_from_record_module()
    return jsonify(data=data)

@app.route('/api/toggle_recording' , methods=['PATCH'])
def toggle_recording():
    data = request.json
    recording = data.get('recording')

    message , status = toggle_recording_camera(recording)
    return jsonify({"success": True, "message": message}), status

@app.route('/api/recording-status/<ip>-<name>', methods=['PATCH'])
def toggle_specific_camera(ip, name):
    try:
        data = request.json
        recording = data.get('recording')
        message, status = recording_status_specific_camera(ip, name, recording)
        return jsonify({"success": True, "message": message}), status

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400
    



# @app.route('/api/devices')  
# @jwt_required()
# def api_devices():
#     data = get_all_devices_from_api()
#     return jsonify(data=data)


# @app.route('/api/file')
# @jwt_required()
# def api_file():
#     file_path = ""
#     send_file = seed_ai_prperties_from_file(file_path)
#     return jsonify(send_file=send_file)