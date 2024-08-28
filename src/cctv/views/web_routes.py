from src import app
from src.cctv.models.model import Zone , Camera
from flask import render_template, request, redirect, url_for, flash , Response , session
from src.cctv.controllers.controller import handle_registration, handle_login , handle_retrieves_zone , handle_add_zone , handle_add_camera  , generate_frames , handle_retrieves_camera , handle_logout , build_rtsp_url , get_online_cameras , get_camera_and_neighbors ,get_alerts_from_api
from flask_login import login_user , logout_user
from werkzeug.utils import secure_filename
import os
from flask_jwt_extended import get_jwt_identity , jwt_required  , verify_jwt_in_request
import datetime




@app.route('/home-page')
@jwt_required()
def home_page():
    camera_id = request.args.get('camera_id', 1, type=int)
    current_user = get_jwt_identity()
    return render_template('index.html', camera_id=camera_id)

@app.route('/', methods=['GET'])
def index():
    try:
        verify_jwt_in_request()
        return redirect(url_for('home_page'))
    except Exception as e:
        return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        success, message = handle_registration(username, password, email)
        if success:
            flash(message=message)
            return redirect(url_for('login'))
        else:
            flash(message=message)
            return redirect(url_for('register'))
    return render_template('register.html')



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user, success, message, response = handle_login(username, password)
        
        if success:
            login_user(user)
            flash(message=message)

            response.headers['Location'] = url_for('home_page')
            response.status_code = 302

            return response  
        
        flash(message=message)
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@jwt_required()
def logout():
    logout_user()

    response = handle_logout()
    
    response.headers['Location'] = url_for('login')  
    response.status_code = 302  
    return response


@app.route('/zones')
@jwt_required()
def zones():
    zones= handle_retrieves_zone()
    return render_template('zones.html' , zones=zones)


@app.route('/add-zone' , methods=['POST' , 'GET'])
@jwt_required()
def add_zone():
    if request.method == 'POST':
        zone_name = request.form.get('zone-name')
        zone_desc = request.form.get('zone-desc')
        success , message = handle_add_zone(zone_name , zone_desc)
        if success:
            flash(message=message)
            return redirect(url_for('zones'))
        else:
            flash(message=message)
            return redirect(url_for('add_zone'))
    return render_template('add-zone.html')



@app.route('/add-camera', methods=['POST', 'GET'])
@jwt_required()
def add_camera():
    if request.method == 'POST':
        camera_ip = request.form.get('cam-ip')
        camera_name = request.form.get('cam-name')
        camera_username = request.form.get('cam-username')
        camera_password = request.form.get('cam-password')
        camera_type = request.form.get('cam-type')
        zone_name = request.form.get('cam-zone')  
        camera_image = None  

        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                camera_image = filename
        success, message = handle_add_camera(camera_ip, camera_name, camera_username, camera_type, camera_password, zone_name, camera_image )
        
        if success:
            flash(message=message)
            return redirect(url_for('cameras'))
        else:
            flash(message=message)
            return redirect(url_for('add_camera'))
    
    zones = Zone.query.all()
    return render_template('add-cam.html', zones=zones)

@app.route('/cameras')
@jwt_required()
def cameras():
    cameras = handle_retrieves_camera()
    return render_template('cameras.html' , cameras=cameras)

@app.route('/camera-view')
def camera_view():
    layout = request.args.get('layout', default=1, type=int)
    
    camera_ip = request.args.get('camera_ip')

    if not camera_ip:
        first_camera = Camera.query.order_by(Camera.camera_id).first()
        if not first_camera:
            return render_template('camera-view.html', cameras=[], camera=None, message="No cameras are currently online", layout=layout)
        camera_ip = first_camera.camera_ip
    
    camera = Camera.query.filter_by(camera_ip=camera_ip).first()
    if not camera:
        return render_template('camera-view.html', cameras=[], camera=None, message="Camera not found", layout=layout)
    
    _, prev_camera_id, next_camera_id = get_camera_and_neighbors(camera.camera_id)

    cameras_in_zone = Camera.query.filter_by(camera_zone=camera.camera_zone).order_by(Camera.camera_id).all()
    
    online_cameras = [get_online_cameras(cameras_in_zone)[0], get_online_cameras(cameras_in_zone)[0], get_online_cameras(cameras_in_zone)[0]]

    cameras_to_display = [online_cameras[i] if i < len(online_cameras) else None for i in range(layout)]

    return render_template(
        'camera-view.html',
        camera=camera,
        cameras=cameras_to_display,
        prev_camera_ip=Camera.query.get(prev_camera_id).camera_ip if prev_camera_id else None,
        next_camera_ip=Camera.query.get(next_camera_id).camera_ip if next_camera_id else None,
        message=None,
        layout=layout
    )



@app.route('/navigate_camera', methods=['POST'])
def navigate_camera():
    # Handle navigation through next or previous buttons
    action = request.form.get('action')
    camera_ip = request.args.get('camera_ip')

    camera = Camera.query.filter_by(camera_ip=camera_ip).first()
    if not camera:
        return redirect(url_for('camera_view'))

    prev_camera_id, next_camera_id = get_camera_and_neighbors(camera.camera_id)
    
    if action == 'next':
        next_camera = Camera.query.get(next_camera_id)
        return redirect(url_for('camera_view', camera_ip=next_camera.camera_ip))
    elif action == 'prev':
        prev_camera = Camera.query.get(prev_camera_id)
        return redirect(url_for('camera_view', camera_ip=prev_camera.camera_ip))

    return redirect(url_for('camera_view'))

@app.route('/video_feed')
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
    )

    return Response(generate_frames(rtsp_url),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/alerts')
def alerts():
    response = get_alerts_from_api()
    data = response['data']

    items_per_page = 5
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * items_per_page
    end = start + items_per_page

    # Paginate the data
    paginated_data = data[start:end]
    total_pages = (len(data) + items_per_page - 1) // items_per_page

    return render_template(
        'alerts.html' , 
        data=paginated_data, 
        page=page, 
        total_pages=total_pages
        )
@app.route('/records' , methods=['POST' , 'GET'])
def records():
    if request.method == 'POST':
        start_time = request.form.get('start-time')
        end_time = request.form.get('end-time')
        session['start_time'] = start_time
        session['end_time'] =end_time
        
        return redirect(url_for('records'))
        
    else:

        start_time= session.get('start_time')
        end_time= session.get('end_time')
        return render_template('records.html', start_time=start_time , end_time=end_time)
