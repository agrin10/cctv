from flask import redirect , url_for , render_template , request , flash   ,session , Response
import os
from werkzeug.utils import secure_filename
from flask_jwt_extended import  jwt_required 
from .camera_controller import generate_frames , handle_add_camera , handle_retrieves_camera ,  get_all_camera_record_with_time , get_camera_and_neighbors , get_online_cameras , build_rtsp_url , search_recorded_files , get_all_alerts 
from .model import Camera , AiProperties 
from src.cctv.zone.model import Zone
from src.cctv.camera import camera_bp




@camera_bp.route('/add-camera', methods=['POST', 'GET'])
@jwt_required()
def add_camera():
    if request.method == 'POST':
        camera_ip = request.form.get('cam-ip')
        camera_name = request.form.get('cam-name')
        camera_username = request.form.get('cam-username')
        camera_password = request.form.get('cam-password')
        camera_type = request.form.get('cam-type')
        zone_name = request.form.get('cam-zone')  
        is_record = request.form.get('is_record')
        camera_image = None  
        ai_properties_list = request.form.getlist('ai_properties[]')

        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(camera.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                camera_image = filename
        success, message , status_code = handle_add_camera(camera_ip, camera_name, camera_username, camera_type, camera_password, zone_name, camera_image, is_record , ai_properties_list)
        
        if success:
            flash(message=message)
            return redirect(url_for('camera.cameras'))
        else:
            flash(message=message)
            return redirect(url_for('camera.add_camera'))
    
    zones = Zone.query.all()
    camera= Camera.query.all()  
    ai_properties = AiProperties.query.all()
    return render_template('add-cam.html', zones=zones , camera=camera , ai_properties=ai_properties)

@camera_bp.route('/cameras')
@jwt_required()
def cameras():
    cameras = handle_retrieves_camera()
    return render_template('cameras.html' , cameras=cameras)

@camera_bp.route('/camera-view')
def camera_view():
    layout = request.args.get('layout', default=1, type=int)
    camera_ip = request.args.get('camera_ip')

    if not camera_ip:
        first_camera = Camera.query.order_by(Camera.camera_id).first()
        if not first_camera:
            return render_template('camera-view.html', cameras=[], message="No cameras are currently online", layout=layout)
        camera_ip = first_camera.camera_ip
    
    camera = Camera.query.filter_by(camera_ip=camera_ip).first()
    if not camera:
        return render_template('camera-view.html', cameras=[], message="Camera not found", layout=layout)
    
    _, prev_camera_id, next_camera_id = get_camera_and_neighbors(camera_ip)

    cameras_in_zone = Camera.query.filter_by(camera_zone=camera.camera_zone).order_by(Camera.camera_id).all()   
    online_cameras = get_online_cameras(cameras_in_zone)  

    
     # Check which cameras are online
    # print(f"Online Cameras: {[cam.camera_ip for cam in online_cameras]}") 

    return render_template(
        'camera-view.html',
        camera=camera,
        cameras=online_cameras,
        prev_camera_ip=Camera.query.get(prev_camera_id).camera_ip if prev_camera_id else None,
        next_camera_ip=Camera.query.get(next_camera_id).camera_ip if next_camera_id else None,
        message=None,
        layout=layout
    )

@camera_bp.route('/video_feed')
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
        camera_port=camera.camera_port
    )

    return Response(generate_frames(rtsp_url),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@camera_bp.route('/alerts/')
def alerts():
    response = get_all_alerts()

    items_per_page = 5
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * items_per_page
    end = start + items_per_page

    paginated_data = response[start:end]
    total_pages = (len(response) + items_per_page - 1) // items_per_page

    return render_template(
        'alerts.html' , 
        data=paginated_data, 
        page=page, 
        total_pages=total_pages
        )

@camera_bp.route('/records', methods=['POST', 'GET'])
def records():
    if request.method == 'POST':
        start_time = request.form.get('start-time')
        end_time = request.form.get('end-time')
        camera_ip= request.form.get('ip')
        camera_name = request.form.get('name')

        session['start_time'] = start_time
        session['end_time'] = end_time

        # videos, status = search_recorded_files(camera_ip=camera_ip, camera_name=camera_name, from_=start_time, to_=end_time)
        data = get_all_camera_record_with_time()

        if status == 200:
            return redirect(url_for('camera.records', ip=camera_ip, name=camera_name))
        else:
            return render_template('records.html', videos=[], start_time=start_time, end_time=end_time)

    else:
        start_time = session.get('start_time')
        end_time = session.get('end_time')
        recorded_files = []

        if start_time and end_time:
            videos, status = search_recorded_files( from_=start_time, to_=end_time)

            if status == 200:
                recorded_files = videos  

        return render_template('records.html', start_time=start_time, end_time=end_time, videos=recorded_files)
