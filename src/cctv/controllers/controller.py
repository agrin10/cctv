from src.cctv.models.model import Users, db , Zone , Camera
from src import login_manager
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_jwt_identity, get_csrf_token
from flask import jsonify , make_response
import cv2
from datetime import datetime ,timedelta
from pytz import timezone 
import pytz
import requests
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)




def handle_registration(username , password , email):
    
    existing_user = Users.query.filter_by(username = username).first()
    existing_email = Users.query.filter_by(email = email).first()
    if existing_user:
        return False , 'username already exists' 
    if password is None:
        return False , 'password is required' 
    if existing_email:
        return False , 'email already exists'
    if len(password) < 8 :
        return False , 'Password must be at least 8 characters long'
    
    new_user = Users(username = username , email = email , password = password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return True , 'registration successful, please login'
    except Exception as e:
            db.session.rollback()
            return False, f'An error occurred: {str(e)}'         



def handle_login(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and user.check_password(password) :
        access_token = create_access_token(identity=user.user_id)
        refresh_token = create_refresh_token(identity=user.user_id, expires_delta=timedelta(days=1))
        
        response = make_response(jsonify({
            "msg": "Login successful"
        }))

        response.set_cookie('access_token_cookie', access_token, httponly=True, samesite='Strict')
        set_refresh_cookies(response, refresh_token)

        
        return user, True, 'Login successful', response 
    return None, False, 'Invalid username or password', None

def handle_logout():
    response = make_response(jsonify({"msg": "Logout successful"}))
    response.delete_cookie('access_token_cookie')
    response.delete_cookie('refresh_token_cookie') 
    return response

def handle_refresh_token():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    resp = 'refresh : true'
    set_access_cookies(resp, access_token)
    return resp, 200

def user_list():
    try:
        users = Users.query.all()
        list_users = []
        list_users=[Users.toDict(user) for user in users]
        return list_users
    except Exception as e:
        db.session.rollback()
        return False, f"An error occurred: {str(e)}"

def handle_add_zone(zone_name , zone_desc):
    existing_zone = Zone.query.filter_by(zone_name = zone_name).first()
    if existing_zone:
        return False , "entered location already exists"
    new_zone = Zone(zone_name = zone_name , zone_desc = zone_desc)
    db.session.add(new_zone)
    db.session.commit()
    return True , 'zone added successfully'

    
def handle_retrieves_zone():
    try:
        zones = Zone.query.all()
        zones = [Zone.toDict(zones) for zones in zones]
        return zones
    except Exception as e:
        db.session.rollback()
        return False, f'An error occurred: {str(e)}'
    

def handle_add_camera(camera_ip, camera_name, camera_username, camera_type, camera_password, zone_name, camera_image , is_record):
    existing_camera = Camera.query.filter_by(camera_ip=camera_ip).first()
    if existing_camera:
        return False, "Camera already exists."
    
    zone = Zone.query.filter_by(zone_name=zone_name).first()
    if zone is None:
        return False, f"Zone '{zone_name}' not found."
    
    label = camera_ip+'-'+camera_name
    
    camera_record= True if is_record == '1' else False
    
    new_camera = Camera(
        camera_ip=camera_ip,
        camera_name=camera_name,
        camera_username=camera_username,
        camera_type=camera_type,
        camera_zone=zone_name, 
        camera_image_path=camera_image, 
        camera_password = camera_password,
        camera_record = camera_record
    )
    

    try:
        db.session.add(new_camera)
        db.session.commit()
        return True, "Camera added successfully."
    except Exception as e:
        db.session.rollback()
        return False, f"An error occurred: {str(e)}"


def handle_retrieves_camera():
    try:
        camera_list = []
        cameras = Camera.query.all()
        for camera in cameras:
            camera_list.append(camera.toDict())
        return  camera_list

    except Exception as e:
        db.session.rollback()
        return False, f'An error occurred: {str(e)}'
    

def build_rtsp_url(camera_ip, camera_username, camera_password):
    return f"rtsp://{camera_username}:{camera_password}@{camera_ip}:554/cam/realmonitor?channel=1&subtype=1"

def generate_frames(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print(f"Cannot open camera with URL: {rtsp_url}")
        return 
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            

            
def get_online_cameras(cameras):

    online_cameras = []

    for camera in cameras:
        rtsp_url = build_rtsp_url(
            camera_ip=camera.camera_ip,
            camera_username=camera.camera_username,
            camera_password=camera.camera_password,
        )
        
        cap = cv2.VideoCapture(rtsp_url)
        if cap.isOpened():
            online_cameras.append(camera)
        cap.release()
    
    return online_cameras

def get_camera_and_neighbors(camera_ip):
    camera = Camera.query.get(camera_ip)
    if not camera:
        return None, None, None

    zone_name = camera.camera_zone  
    cameras_in_zone = Camera.query.filter_by(camera_zone=zone_name).order_by(Camera.camera_ip).all()
    
    current_camera_index = next((index for index, c in enumerate(cameras_in_zone) if c.camera_ip == camera_ip), None)
    
    if current_camera_index is None:
        return None, None, None

    prev_camera_id = cameras_in_zone[current_camera_index - 1].camera_ip if current_camera_index > 0 else cameras_in_zone[-1].camera_ip
    next_camera_id = cameras_in_zone[(current_camera_index + 1) % len(cameras_in_zone)].camera_ip

    return camera, prev_camera_id, next_camera_id   
def get_alerts_from_api():
    alert_url = "http://192.168.10.107/alerts/"
    response = requests.get(alert_url)

    response.raise_for_status()
    data = response.json()

    return data

def get_records_from_api(start_time , end_time):
    records_url = "http://192.168.10.108/devices/192.168.10.247-test/search_files"

    if not start_time and end_time:
        return "error: Start time or end time is missing"
    try:
        start_time_gmt , end_time_gmt = make_time_gmt(start_time, end_time)

        params={
            'from':start_time_gmt,
            'to':end_time_gmt
        }
        print(f"Request params: {params}")

        response = requests.get(records_url , params=params)

        response.raise_for_status()
        data= response.json()
        return data
    

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"An error occurred: {err}"}


def make_time_gmt(start_time , end_time):
    if not start_time and end_time :
        return "error: Start time or end time is missing" , 400
    
    input_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    start_datetime = datetime.strptime(start_time, input_format)
    end_datetime = datetime.strptime(end_time, input_format)

    local_tz =  timezone('Asia/Tehran')

    start_datetime_local  = local_tz.localize(start_datetime)
    end_datetime_local = local_tz.localize(end_datetime)

    # Convert to UTC
    start_datetime_utc = start_datetime_local.astimezone(pytz.utc)
    end_datetime_utc = end_datetime_local.astimezone(pytz.utc)

    start_time_iso = start_datetime_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3]
    end_time_iso = end_datetime_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3] 


    return start_time_iso , end_time_iso