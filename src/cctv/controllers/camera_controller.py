# from src.cctv.models.model import Users, db , Zone , Camera , AiProperties
# from src import login_manager
# from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_jwt_identity, get_csrf_token
# from flask import jsonify , make_response
# import cv2
# from datetime import datetime ,timedelta
# from pytz import timezone 
# import pytz
# import requests



    

    
# def handle_add_camera(camera_ip:str, camera_name:str, camera_username:str, camera_type:str, camera_password:str, zone_name:str, camera_image:str , is_record:bool , ai_properties:list):
#     existing_camera = Camera.query.filter_by(camera_ip=camera_ip).first()
#     if existing_camera:
#         return False, "Camera already exists."
    
#     zone = Zone.query.filter_by(zone_name=zone_name).first()
#     if zone is None:
#         return False, f"Zone '{zone_name}' not found."
    
#     label = camera_ip+'-'+camera_name
    
#     camera_record= True if is_record == '1' else False

    
    
#     new_camera = Camera(
#         camera_ip=camera_ip,
#         camera_name=label,
#         camera_username=camera_username,
#         camera_type=camera_type,
#         camera_zone=zone_name, 
#         camera_image_path=camera_image, 
#         camera_password = camera_password,
#         camera_record = camera_record
#     )
    

#     try:
#         db.session.add(new_camera)
#         db.session.commit()
#         return True, "Camera added successfully."
#     except Exception as e:
#         db.session.rollback()
#         return False, f"An error occurred: {str(e)}"


# def handle_retrieves_camera():
#     try:
#         camera_list = []
#         cameras = Camera.query.all()
#         for camera in cameras:
#             camera_list.append(camera.toDict())
#         return  camera_list

#     except Exception as e:
#         db.session.rollback()
#         return False, f'An error occurred: {str(e)}'
    

# def build_rtsp_url(camera_ip, camera_username, camera_password):
#     return f"rtsp://{camera_username}:{camera_password}@{camera_ip}:554/cam/realmonitor?channel=1&subtype=1"

# def generate_frames(rtsp_url):
#     cap = cv2.VideoCapture(rtsp_url)
#     if not cap.isOpened():
#         print(f"Cannot open camera with URL: {rtsp_url}")
#         return 
    
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            

            
# def get_online_cameras(cameras):

#     online_cameras = []

#     for camera in cameras:
#         rtsp_url = build_rtsp_url(
#             camera_ip=camera.camera_ip,
#             camera_username=camera.camera_username,
#             camera_password=camera.camera_password,
#         )
        
#         cap = cv2.VideoCapture(rtsp_url)
#         if cap.isOpened():
#             online_cameras.append(camera)
#         cap.release()
    
#     return online_cameras

# def get_camera_and_neighbors(camera_ip):
#     camera = Camera.query.get(camera_ip)
#     if not camera:
#         return None, None, None

#     zone_name = camera.camera_zone  
#     cameras_in_zone = Camera.query.filter_by(camera_zone=zone_name).order_by(Camera.camera_ip).all()
    
#     current_camera_index = next((index for index, c in enumerate(cameras_in_zone) if c.camera_ip == camera_ip), None)
    
#     if current_camera_index is None:
#         return None, None, None

#     prev_camera_id = cameras_in_zone[current_camera_index - 1].camera_ip if current_camera_index > 0 else cameras_in_zone[-1].camera_ip
#     next_camera_id = cameras_in_zone[(current_camera_index + 1) % len(cameras_in_zone)].camera_ip

#     return camera, prev_camera_id, next_camera_id   
