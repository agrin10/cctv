from .camera_controller import  handle_add_camera , handle_retrieves_camera , search_recorded_files , get_alerts_from_api , handle_edit_camera , handle_delete_camera , get_all_cameras_from_record_module, toggle_recording_camera , recording_status_specific_camera , build_rtsp_url
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from src.camera import camera_bp
from src.permissions import permission_required




@camera_bp.route('/api/add-camera', methods=['POST' ])
@permission_required(['create'])
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


@camera_bp.route('/api/edit-camera', methods=['PATCH'])
@permission_required(['edit'])
@jwt_required()
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

@camera_bp.route('/api/delete-camera/<ip>-<name>' ,methods=['DELETE'])
@permission_required(['delete'])
@jwt_required()
def api_delete_camera(ip , name):
    status_code , success , message = handle_delete_camera(ip, name)
    if not success:
        return jsonify({"success": False, "message": message}), status_code
    return jsonify({"success": True, "message": message}), status_code
    

@camera_bp.route('/api/cameras')
@permission_required(['view'])
@jwt_required()
def api_cameras():
    cameras = handle_retrieves_camera()
    return jsonify(cameras = cameras)


@camera_bp.route('/api/alerts') 
@permission_required(['view'])
@jwt_required()
def api_alerts():
    data = get_alerts_from_api()
    return jsonify(data)

@camera_bp.route('/api/search-files/<ip>-<name>')
@jwt_required()
@permission_required(['view'])
def search_files(ip:str , name:str):
    start_time = request.args.get('from')
    end_time = request.args.get('to')
    data = search_recorded_files(camera_ip=ip , camera_name=name, from_=start_time , to_=end_time)
    return jsonify(data=data)


@camera_bp.route('/api/get-all-cameras-record-module')
def cameras_record():
    data = get_all_cameras_from_record_module()
    return jsonify(data=data)

@camera_bp.route('/api/toggle_recording' , methods=['PATCH'])
@permission_required(['edit'])
@jwt_required()
def toggle_recording():
    data = request.json
    recording = data.get('recording')

    message , status = toggle_recording_camera(recording)
    return jsonify({"success": True, "message": message}), status

@camera_bp.route('/api/api/recording-status/<ip>-<name>', methods=['PATCH'])
@permission_required(['edit'])
@jwt_required()
def toggle_specific_camera(ip, name):
    try:
        data = request.json
        recording = data.get('recording')
        message, status = recording_status_specific_camera(ip, name, recording)
        return jsonify({"success": True, "message": message}), status

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
