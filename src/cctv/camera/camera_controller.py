from .model import  db ,  Camera , AiProperties
from sqlalchemyseeder import ResolvingSeeder
import json
from datetime import datetime
import cv2
from .api_controller import check_ai_module_api , check_modules_status , add_camera_api,check_recording_api , delete_camera_api , edit_camera , toggle_record_option_for_all , toggle_recording_specific_camera , get_all_cameras_from_record_module ,get_alerts_from_api , get_records_from_api , build_rtsp_url
from src.cctv.zone.model import Zone



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
        
    response ,status_code = add_camera_api(camera_ip=camera_ip ,camera_name=camera_name , username=camera_username , password=camera_password , ai_properties=ai_properties,run_detection=run_detection)
    if status_code in range(400 , 600):
        return False , response

    
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
        ai_instance = AiProperties(name=ai_property)  
        new_camera.ai_properties.append(ai_instance)

    try:
        db.session.add(new_camera)  
        db.session.commit()
        return True, "Camera added successfully." 
    except Exception as e:
        db.session.rollback()
        return False, f"An error occurred: {str(e)}"


    
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
    

def recording_status_specific_camera(ip:str , name:str , bool:bool):
    success , message , status = toggle_recording_specific_camera(ip , name , bool)
    if success:
        return message , status
    return message , status



def search_recorded_files(camera_ip: str, camera_name: str, from_: str, to_: str):
    response, status_code = get_records_from_api(ip=camera_ip, name=camera_name, start_time=from_, end_time=to_)
    
    if status_code == 200:
        files = response.get('data', {}).get('files', [])
        return files, status_code
    else:
        return [], status_code
    

