from flask import redirect, url_for, render_template, request, flash, session, Response , jsonify
import os
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
from .camera_controller import generate_frames, handle_add_camera, handle_retrieves_camera, get_camera_and_neighbors, get_online_cameras, build_rtsp_url, search_recorded_files, get_all_alerts  ,capture_image_from_latest_frame , handle_edit_camera, handle_delete_camera , get_all_camera_record_with_time
from .model import Camera, AiProperties
from src.zone.model import Zone
from src.camera import camera_bp
import time
from src.permissions import permission_required

@camera_bp.route('/', methods=['POST'])
@permission_required(['create'])
@jwt_required()
def add_camera():
    print(request.form)
    camera_ip = request.form.get('ipAddress')
    camera_name = request.form.get('deviceName')
    camera_username = request.form.get('camera_username')
    camera_password = request.form.get('camera_password')  
    camera_type = request.form.get('deviceType')

    zone_name = request.form.get('zone_name')  
    is_record = request.form.get('is_record')  
    ai_properties_list = request.form.getlist('ai_properties[]') 
    is_record = True if is_record == '1' else False

    print(f'{camera_ip} , {camera_name} , {camera_password} , {camera_username} , {camera_type} , {zone_name} , {ai_properties_list}, {is_record}')

    success, message = handle_add_camera(
        camera_ip=camera_ip,
        camera_name=camera_name,
        camera_username=camera_username,
        camera_type=camera_type,
        camera_password=camera_password,
        zone_name=zone_name,
        recording=is_record,
        ai_properties=ai_properties_list
    )

    if success:
        flash(message=message)
        return redirect(url_for('camera.cameras'))
    else:
        flash(message=message)
        return message, 400



def get_camera_by_ip(camera_ip):
    camera = Camera.query.filter_by(camera_ip=camera_ip).first()
    if camera:
        return {
            'camera_ip': camera.camera_ip,
            'device_name': camera.camera_name,
            'device_type': camera.camera_type,
            'username': camera.camera_username,
            'password': camera.camera_password,
            'zones': camera.zone.zone_name,
            'ai_properties': [prop.name for prop in camera.ai_properties],
            'recording': camera.camera_record
        }
    else:
        return None

@camera_bp.route('/', methods=["PATCH"])  
def edit_camera():
    if request.method == "PATCH":
        data = request.json
        print('Received data:', data)
        
        camera_ip = data.get('oldIpAddress')
        print(camera_ip)
        old_camera_data = get_camera_by_ip(camera_ip)
        if not old_camera_data:
            return jsonify({"success": False, "message": "Camera not found"}), 404

        camera_new_ip = data.get('newIpAddress', old_camera_data['camera_ip'])
        
        camera_new_name = data.get('deviceName', old_camera_data['device_name'])
        camera_new_username = data.get('camera_username', old_camera_data['username'])
        camera_new_password = data.get('camera_password', old_camera_data['password'])

        camera_zone = data.get('camera_zones', old_camera_data['zones'])
        print(f'{camera_zone} , and the username of camera {camera_new_username}  ')

        recording = data.get('recording', old_camera_data['recording'])
        ai_properties = data.get('ai_properties', old_camera_data['ai_properties'])
        
        recording= True if recording == 'yes' else False
        success, message = handle_edit_camera(
            camera_ip=camera_ip, new_ip=camera_new_ip,
            name=old_camera_data['device_name'], new_name=camera_new_name,
            username=old_camera_data['username'], new_username=camera_new_username,
            password=old_camera_data['password'], new_password=camera_new_password,
            camera_zone=camera_zone,
            recording=recording, ai_properties=ai_properties
        )

        if not success:
            return jsonify({"success": False, "message": message}), 400

        return jsonify({"success": True, "message": "Camera updated successfully!"}), 200
    
    else:
        return jsonify({"success": False, "message": "Invalid request method."}), 405
    


@camera_bp.route('/delete-camera/ip=<ip>&name=<name>', methods=['DELETE'])
@permission_required(['delete'])
@jwt_required()
def delete_camera(ip, name):
    print(f'ip is {ip} and name is {name}')
    success, message = handle_delete_camera(ip, name)
    if not success:
        return jsonify({"success": False, "message": message}), 500
    return jsonify({"success": True, "message": message}), 200

    



@camera_bp.route('/')
@permission_required(['view' ])
@jwt_required()
def cameras():
    page = request.args.get('page', 1, type=int)
    zones = Zone.query.all()
    cameras_list = Camera.query.all()
    ai_properties = AiProperties.query.all()

    page = request.args.get('page', 1, type=int)  
    per_page = 12  
    cameras = Camera.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('cameras.html',zones=zones, camera=cameras_list, ai_properties=ai_properties , pagination=cameras , cameras=cameras.items)





@camera_bp.route('/video_feed')
@jwt_required()
@permission_required(['view' ,'overall view' , 'playback'])
def video_feed():
    camera_ip = request.args.get('camera_ip')
    if not camera_ip:
        return "Camera not found", 404

    camera = Camera.query.filter_by(camera_ip=camera_ip).first()
    if not camera:
        return "Camera not found", 404

    rtsp_url = build_rtsp_url(
        camera_ip=camera.camera_ip,
        camera_username=camera.camera_username,
        camera_password=camera.camera_password,
        # camera_port=camera.camera_port
    )

    return Response(generate_frames(rtsp_url),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@camera_bp.route('/capture_image', methods=['POST'])
@jwt_required()
@permission_required(['create' , 'playback' , 'overall view'])
def capture_image_route():
    """Route to capture an image from the video feed."""
    camera_ip = request.form.get('camera_ip')
    if not camera_ip:
        return "Camera not found", 404

    camera = Camera.query.filter_by(camera_ip=camera_ip).first()
    if not camera:
        return "Camera not found", 404

    try:
        # Generate a unique filename using timestamp
        timestamp = int(time.time())
        filename = f'captured_image_{timestamp}.png'
        file_path = capture_image_from_latest_frame(filename)
        
        # Redirect back to the camera view with the filename parameter
        return redirect(url_for('camera.camera_view', camera_ip=camera_ip, filename=filename))

    except ValueError as e:
        return str(e), 500

@camera_bp.route('/camera-view')
@jwt_required()
@permission_required(['view', 'overall view', 'playback'])
def camera_view():
    layout = request.args.get('layout', default=1, type=int)
    page = request.args.get('page', default=1, type=int)
    camera_ip = request.args.get('camera_ip')
    zone_id = request.args.get('zone_id')

    if not camera_ip and not zone_id:
        latest_camera = Camera.query.order_by(Camera.camera_id.desc()).first()
        if latest_camera:
            camera_ip = latest_camera.camera_ip
            zone_id = latest_camera.camera_zone
        else:
            return render_template('camera-view.html', cameras=[], message="No cameras available", layout=layout)

    if camera_ip:
        camera = Camera.query.filter_by(camera_ip=camera_ip).first()
        if camera:
            zone_id = camera.camera_zone  

    cameras_in_zone = Camera.query.filter_by(camera_zone=zone_id).order_by(Camera.camera_id).all()

    per_page = layout
    start = (page - 1) * per_page
    paginated_cameras = cameras_in_zone[start:start + per_page]

    online_cameras = get_online_cameras(paginated_cameras)
    placeholders_needed = layout - len(online_cameras)
    total_pages = (len(cameras_in_zone) // per_page) + (1 if len(cameras_in_zone) % per_page != 0 else 0)

    return render_template(
        'camera-view.html',
        camera=camera,
        cameras=online_cameras,
        message=None,
        layout=layout,
        placeholders_needed=placeholders_needed,
        current_page=page,
        next_page=page + 1 if page < total_pages else None,
        prev_page=page - 1 if page > 1 else None,
        total_pages=total_pages
    )


@camera_bp.route('/alerts/')
@jwt_required()
@permission_required(['view'])
def alerts():
    response = get_all_alerts()

    items_per_page = 5
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * items_per_page
    end = start + items_per_page

    paginated_data = response[start:end]
    total_pages = (len(response) + items_per_page - 1) // items_per_page

    return render_template(
        'alerts.html',
        data=paginated_data,
        page=page,
        total_pages=total_pages
    )
@camera_bp.route('/records', methods=['POST', 'GET'])
@jwt_required()
def records():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print("Data type:", type(data))  
            print("Data:", data)

            start_date = data.get('start_date')
            end_date = data.get('end_date')
            start_time = data.get('start_time', "00:00:00") 
            end_time = data.get('end_time', "23:59:59")     
            
            _from = f'{start_date} {start_time}'
            _to = f'{end_date} {end_time}'

            # devices, status_code = get_all_camera_record_with_time(from_=_from, to_=_to)
            # print("Devices type:", type(devices))

            # return jsonify({"status": "success", "devices": devices}), status_code
            return jsonify('devices')

        except Exception as e:
            print("Error:", e)
            return jsonify({"status": "error", "message": "Failed to process data"}), 500
    else:
        
        # devices, _ = get_all_camera_record_with_time(from_=None, to_=None)  # Get all records
        layout = request.args.get('layout', 4, type=int)  
        page = request.args.get('page', 1, type=int)     
        total_pages = 2 
        # total_pages = len(devices)

        return render_template(
            'records.html',
            layout=layout,
            page=page,
            total_pages=total_pages,
            current_page=page,
            # devices=devices,
            prev_page=page - 1 if page > 1 else None,
            next_page=page + 1 if page < total_pages else None,
        )

    
    
@camera_bp.route('/full-screen')
def full_screen():
    layout = request.args.get('layout', default=16, type=int)  
    all_cameras = Camera.query.order_by(Camera.camera_id).all()
    online_cameras = get_online_cameras(all_cameras)

    for camera in all_cameras:
        camera.is_online = camera in online_cameras
    placeholders_needed = layout - len(online_cameras)

    return render_template(
        'fullscreen.html',
        cameras=all_cameras,
        layout=layout,
        placeholders_needed=placeholders_needed
    )

@camera_bp.route('/calendar')
def calendar():
    return render_template('calendar.html')
# 2024-08-27 15:58:31


