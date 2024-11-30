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
from src.camera.schema import AddCameraSchema , EditCameraSchema
from marshmallow import ValidationError



@camera_bp.route('/', methods=['POST'])
@permission_required(['create'])
@jwt_required()
def add_camera():
    schema = AddCameraSchema()
    try:
        form_data = request.form.to_dict(flat=True)  
        
        form_data["ai_properties"] = request.form.getlist("ai_properties") 

        
        if "is_record" in form_data:
            form_data["is_record"] = form_data["is_record"].lower() in ["true", "1", "yes"]
        print(form_data)
        data = schema.load(form_data)
        
    except ValidationError as err:
        return jsonify({"success": False, "errors": err.messages}), 400

    success, message = handle_add_camera(
        camera_ip=data["ipAddress"],
        camera_name=data["deviceName"],
        camera_username=data["camera_username"],
        camera_type=data["deviceType"],
        camera_password=data["camera_password"],
        zone_name=data["zone_name"],
        recording=data["is_record"],
        ai_properties=data["ai_properties"],  
    )

    if success:
        flash(message=message)
        return redirect(url_for("camera.cameras"))
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

@camera_bp.route('/' , methods=["PATCH"])
@jwt_required()
@permission_required(['edit' , 'view'])
def edit_camera():
    schema = EditCameraSchema() 

    if request.is_json:
        data = request.json  
        print("Received data:", data)
    else:
        data = request.form.to_dict()

    try:
        validated_data = schema.load(data)
        print("Validated data:", validated_data)
    except ValidationError as err:
        print(f'success: {False} , error: {err.messages}')
        return jsonify({"success": False, "errors": err.messages}), 400

    # Extract old and new data
    old_ip = validated_data.get("oldIpAddress")
    new_ip = validated_data.get("newIpAddress")
    new_name = validated_data.get("deviceName")
    new_username = validated_data.get("camera_username")
    new_password = validated_data.get("camera_password")
    new_zones = validated_data.get("camera_zones", [])
    new_recording = validated_data.get("recording") == "yes"
    new_ai_properties = validated_data.get("ai_properties", [])

    old_camera_data = get_camera_by_ip(old_ip)
    if not old_camera_data:
        return jsonify({"success": False, "message": "Camera not found"}), 404

    old_name = old_camera_data.get("device_name")
    old_username = old_camera_data.get("username")
    old_password = old_camera_data.get("password")

    # Handle camera update
    success, message = handle_edit_camera(
        camera_ip=old_ip, name=old_name, username=old_username,
        password=old_password, camera_zone =new_zones , 
        new_ip=new_ip, new_name=new_name, new_username=new_username,
        new_password=new_password, recording=new_recording,ai_properties=new_ai_properties 
    )

    if not success:
        return jsonify({"success": False, "message": message}), 400

    return jsonify({"success": True, "message": message}), 200


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
            return render_template('camera-view.html', cameras=[], message="No cameras available", layout=layout , total_pages=0)

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


