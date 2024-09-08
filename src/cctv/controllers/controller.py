from src.cctv.models.model import Users, db , Zone , Camera , AiProperties
from src import login_manager
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_jwt_identity, get_csrf_token
from flask import jsonify , make_response
import cv2
from datetime import datetime ,timedelta
from pytz import timezone 
import pytz
import requests
from sqlalchemyseeder import ResolvingSeeder
import json
import re





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
    

def seed_ai_properties():
    session = db.session
    seeder = ResolvingSeeder(session)
    seeder.register(AiProperties)

    try:
        # Load new properties from the JSON file with UTF-8 encoding
        with open("src/static/names.json", "r", encoding="utf-8") as file:
            new_properties = json.load(file)

        for property_data in new_properties:
            if property_data['target_class'] == 'AiProperties':
                existing_property = session.query(AiProperties).filter_by(name=property_data['data']['name']).first()
                
                if existing_property:   
                    continue

                new_property = AiProperties(name=property_data['data']['name'], label=property_data['data']['label'])
                session.add(new_property)

        db.session.commit()
        print("AI properties successfully committed to the database.")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
    finally:
        db.session.close()


recording_url = 'http://192.168.10.108/'
ai_url = 'http://192.168.10.107/'
payload = {}
header = {
    'Content-Type': 'application/json'
}


def check_recording_api():
    try:
        response  = requests.get(recording_url)
        if response.status_code in range(500 , 599):
            return False 
    except Exception as e:
        return False
    return True

def check_ai_module_api():
    try:
        response  = requests.get(ai_url)
        if response.status_code in range(500,599):
            return False
    except Exception as e:
        print('AI module:' + e)
        return False
    return True 

def check_modules_status():
    if not check_ai_module_api or not check_recording_api():
        return False
    return True

    

def add_camera_api(camera_ip: str, camera_name: str, username: str, password: str, ai_properties: list, run_detection: bool):
    label = f"{camera_ip}-{camera_name}"
    rtsp_url = build_rtsp_url(camera_ip, username, password)
    
    payload = {
        "label": label,
        "input": rtsp_url
    }
    
    ai_payload = {
        "label": label, 
        "input": rtsp_url,
        "detections": ai_properties,
        "run_detection": run_detection
    }

    if not check_modules_status():
        return "Modules are not available", 500
    
    try:
        ai_response = requests.post(ai_url + "devices/", headers=header, json=ai_payload)
        ai_response.raise_for_status()
        
        print(f"AI Response Status Code: {ai_response.status_code}")
        print(f"AI Response Body: {ai_response.text}")

        print("Sending payload to recording URL:", payload)
        response = requests.post(recording_url + "devices/", headers=header, json=payload)
        response.raise_for_status()

        if ai_response.status_code in range(400, 600):
            return None, 506

        return ai_response.json(), ai_response.status_code

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while calling the API: {e}")
        return f"An error occurred: {str(e)}", 500
    
def handle_add_camera(
        camera_ip:str, camera_name:str, camera_username:str, camera_type:str, camera_password:str, zone_name:str, camera_image:str , recording:bool , ai_properties:list , camera_port:int
        ):
    existing_camera = Camera.query.filter_by(camera_ip=camera_ip).first()
    if existing_camera:
        return False, "Camera already exists."
    
    zone = Zone.query.filter_by(zone_name=zone_name).first()
    if zone is None:
        return False, f"Zone '{zone_name}' not found."
    
    label = camera_ip+'-'+camera_name
    run_detection = False if ai_properties == [] else True
    if recording:
        success , message , status_code = toggle_recording_specific_camera(ip=camera_ip , name=camera_name ,bool='true')
        if status_code == 500:
            recording = False


        if status_code == 500:
            return False, "Modules are not available."
        
    # response ,status_code = add_camera_api(camera_ip=camera_ip ,camera_name=camera_name , username=camera_username , password=camera_password , ai_properties=ai_properties,run_detection=run_detection)
    # if status_code in range(400 , 600):
    #     return False , response

    
    new_camera = Camera(
        camera_ip=camera_ip,
        camera_name=label,
        camera_username=camera_username,
        camera_type=camera_type,
        camera_zone=zone_name, 
        camera_image_path=camera_image, 
        camera_password = camera_password,
        camera_record = recording,
        camera_port = camera_port
    )
    
    for ai_property in ai_properties:
        ai_instance = AiProperties(name=ai_property)  # Create an instance
        new_camera.ai_properties.append(ai_instance)

    try:
        db.session.add(new_camera)
        db.session.commit()
        return True, "Camera added successfully." 
    except Exception as e:
        print(f'ai_url:{ai_url}')
        db.session.rollback()
        return False, f"An error occurred: {str(e)}"

def edit_camera(camera_ip:str, camera_new_ip:str, camera_name:str, camera_new_name:str, username:str, new_username:str, password:str, new_password:str,recording:bool, ai_properties:list, run_detection:bool):

    label = f"{camera_ip}-{camera_name}"
    new_label = f"{camera_new_ip}-{camera_new_name}"

    rtsp_url = build_rtsp_url(camera_ip, username, password)
    new_rtsp_url = build_rtsp_url(camera_new_ip, new_username, new_password)

    # Define payloads based on whether the label has changed
    if label == new_label:
        payload = {"recording": recording}
        ai_payload = {
            "input": rtsp_url,
            "detections": ai_properties,
            "run_detection": run_detection
        }
    else:
        payload = {
            "label": new_label,
            "recording": recording
        }
        ai_payload = {
            "label": new_label,
            "input": new_rtsp_url,
            "detections": ai_properties,
            "run_detection": run_detection
        }

    if not check_modules_status():
        return None, 500

    try:
        response = requests.patch(recording_url + "devices", headers=header, json=payload)
        response.raise_for_status() 

        ai_response = requests.patch(ai_url + "devices", headers=header, json=ai_payload)
        ai_response.raise_for_status()

        return {
            "recording_module": response.json(),
            "ai_module": ai_response.json()
        }, 200

    except requests.RequestException as e:
        return False, f"Error in external service: {str(e)}"

def handle_edit_camera(camera_ip: str, new_ip: str, name: str, new_name: str, username: str, new_username:str, password: str,new_password:str , camera_type: str, camera_zone: str, recording: bool, ai_properties: list):
    camera = Camera.query.filter_by(camera_ip=camera_ip).first()
    
    if not camera:
        return False, "Camera not found."

    run_detection = False if ai_properties == [] else True

    # Fetch the AI properties from the database
    ai_property_instances = AiProperties.query.filter(AiProperties.name.in_(ai_properties)).all()

    response, status_code = edit_camera(camera_ip=camera_ip,
    camera_new_ip=new_ip,
    camera_name=name,
    camera_new_name=new_name,
    username=username,
    new_username=new_username,
    password=password,
    new_password=new_password,
    recording=recording,
    ai_properties=ai_property_instances,
    run_detection=run_detection
    )
    
    if status_code in range(400, 600):
        return response, status_code  
    
    camera.camera_ip = new_ip
    camera.camera_name = new_name
    camera.camera_type = camera_type
    camera.camera_zone = camera_zone
    camera.camera_record = recording
    camera.ai_properties = ai_property_instances   

    try:
        db.session.commit()
        return True, "Camera updated successfully."
    except Exception as e:
        db.session.rollback()
        return False, f"Update failed: {str(e)}"


def delete_camera_api(camera_ip:str , camera_name:str):
    label = f'{camera_ip} - {camera_name}'
    if not check_modules_status():
        return 500
    
    #sending delete requeest to ai api
    ai_response = requests.delete(ai_url + "devices" + label , headers=header)
    ai_response.raise_for_status()

    return ai_response , True , "camera deleted successfuly."

def handle_delete_camera(ip:str , name:str):
    # TODO: we cant delete camera from the recording API
    status_code , success ,response   = delete_camera_api(ip , name)
    if status_code in range(400, 600):
        return response , status_code
    
    camera = Camera.query.filter_by(camera_ip = ip ).first()
    try:
        db.session.delete(camera)
        db.session.commit()
        return True , "Camera deleted successfully."
    except Exception as e:
        db.session.rollback()
        return False , f"Delete failed: {str(e)}"

def get_all_cameras_from_record_module():
    if not check_modules_status():
        return None , 500
    response = requests.get(recording_url + "devices" , headers=header, json=payload)
    response.raise_for_status()
    return response.json(), response.status_code
    
def toggle_recording_specific_camera(ip:str , name:str , bool:bool):
    payload = {"recording" :bool}
    camera_label = f'{ip}-{name}'
    if not check_modules_status():
        return 500
    response = requests.patch(recording_url + "devices/"+ camera_label , headers=header , json=payload)
    response.raise_for_status()
    return True , "Recording toggled successfully." , 200

def recording_status_specific_camera(ip:str , name:str , bool:bool):
    success , message , status = toggle_recording_specific_camera(ip , name , bool)
    if success:
        return message , status
    return message , status


def toggle_record_option_for_all(bool:str):
    payload = {"recording" :bool}
    cameras , status_code = get_all_cameras_from_record_module()
    if status_code == 500:
        return status_code
    for camera in cameras['data']['devices']:
        camera_label = camera['label']
        response = requests.patch(recording_url + "devices/"+camera_label , headers=header , json=payload)
        response.raise_for_status()
    return True , "Recording toggled successfully." , status_code


def toggle_recording_camera(bool:bool):
    success ,message ,status = toggle_record_option_for_all(bool)
    if success:
        return message , status
    return message , status


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
    

def build_rtsp_url(camera_ip, camera_username, camera_password , camera_port):
    return f"rtsp://{camera_username}:{camera_password}@{camera_ip}:{camera_port}/cam/realmonitor?channel=1&subtype=1"

def generate_frames(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)
    
    if not cap.isOpened():
        print(f"Cannot open camera with URL: {rtsp_url}")
        cap = cv2.VideoCapture(rtsp_url, apiPreference=cv2.CAP_ANY, params=[cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 2000])
    
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
            camera_port=camera.camera_port
        )
        
        cap = cv2.VideoCapture(rtsp_url)
        if cap.isOpened():
            online_cameras.append(camera)
            print(f"Camera Online: {camera.camera_ip}")  
        else:
            print(f"Camera Offline: {camera.camera_ip}")  
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
    response = requests.get(ai_url+"alerts" , headers=header )
    response.raise_for_status()
    data = response.json()

    return data , response.status_code
def get_all_alerts():
    response , status_code = get_alerts_from_api()

    if status_code == 200:
        return response['data'], status_code
    else:
        return [], status_code
    
# def get_alerts_by_camera(camera_ip):
#     response , status_code = get_alerts_from_api()
#     if status_code == 200:


def get_all_camera_record_with_time(from_ , to_):
    make_response = get_all_cameras_from_record_module()
    if make_response:
        return make_response['data']['data']['devices'] , 200
    else:
        return [] , 500
    

def get_records_from_api(ip: str, name: str, start_time, end_time):
    if not start_time or not end_time:
        return "error: Start time or end time is missing", 400  

    try:
        if is_iso_format(start_time) and is_iso_format(end_time):
            start_time_gmt = start_time
            end_time_gmt = end_time
        else:
            start_time_gmt , end_time_gmt=make_time_gmt(start_time=start_time , end_time=end_time)

        params = {
            'from': start_time_gmt,
            'to': end_time_gmt
        }
        print(f"Request params: {params}")

        search_file_url = recording_url + "devices/" + ip + "-" + name + "/search_files"
        
        if not check_modules_status():
            return None, 500
            
        response = requests.get(search_file_url, headers=header, params=params)
        response.raise_for_status()

        data = response.json()
        print(f"Response data from API: {data}")  

        return data, response.status_code

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}, response.status_code  
    except Exception as err:
        return {"error": f"An error occurred: {err}"}, 500  

def search_recorded_files(camera_ip: str, camera_name: str, from_: str, to_: str):
    response, status_code = get_records_from_api(ip=camera_ip, name=camera_name, start_time=from_, end_time=to_)
    
    if status_code == 200:
        files = response.get('data', {}).get('files', [])
        return files, status_code
    else:
        return [], status_code
    

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


def is_iso_format(date_string: str) -> bool:
    # Regular expression to match the ISO 8601 date format
    iso_regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$'
    return bool(re.match(iso_regex, date_string))