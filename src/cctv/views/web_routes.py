from src import app
from src.cctv.models.model import Zone , Camera
from flask import render_template, request, redirect, url_for, flash , Response
from src.cctv.controllers.controller import handle_registration, handle_login , handle_retrieves_zone , handle_add_zone , handle_add_camera  , generate_frames , handle_retrieves_camera
from flask_login import login_user
from werkzeug.utils import secure_filename
import os


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


@app.route('/zones')
def zones():
    zones= handle_retrieves_zone()
    return render_template('zones.html' , zones=zones)


@app.route('/add-zone' , methods=['POST' , 'GET'])
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
def cameras():
    cameras = Camera.query.all()
    return render_template('cameras.html' , cameras=cameras)


@app.route('/camera-view')
def camera_view():
    return render_template('camera-view.html' )



@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')