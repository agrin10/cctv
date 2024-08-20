from src.cctv.models.model import Users, db , Zone , Camera
from src import login_manager ,app
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_jwt_identity, get_csrf_token
from flask import jsonify , make_response
import cv2
import datetime


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
    
    new_user = Users(username = username , email = email)
    new_user.set_password(password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return True , 'registration successful, please login'
    except Exception as e:
            db.session.rollback()
            return False, f'An error occurred: {str(e)}'         




def handle_login(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.user_id)
        refresh_token = create_refresh_token(identity=user.user_id, expires_delta=datetime.timedelta(days=1))
        
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
    

def handle_add_camera(camera_ip, camera_name, camera_username, camera_type, camera_password, zone_name, camera_image):
    existing_camera = Camera.query.filter_by(camera_ip=camera_ip).first()
    if existing_camera:
        return False, "Camera already exists."
    
    zone = Zone.query.filter_by(zone_name=zone_name).first()
    if zone is None:
        return False, f"Zone '{zone_name}' not found."
    


    new_camera = Camera(
        camera_ip=camera_ip,
        camera_name=camera_name,
        camera_username=camera_username,
        camera_type=camera_type,
        camera_zone=zone_name, 
        camera_image_path=camera_image
    )
    new_camera.set_password(camera_password)

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
    

def generate_frames():
    rtsl_url = app.config['RTSP_URL']
    cap = cv2.VideoCapture(rtsl_url)
    while True:
        success, frame = cap.read() 
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()  
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            


            