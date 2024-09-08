# from src.cctv.models.model import Users, db , Zone , Camera
# from app import app
# from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_jwt_identity, get_csrf_token
# from flask import jsonify , make_response
# import cv2
# import pytz
# import requests


# ai_url = app.config['AI_URL']
# recording_url = app.config['RECORDING_URL']
# input_filename = 'coco.names'

# def parse_data_from_file(filename):
#     filename = "coco.names"
#     with open(filename ,'r') as file:
#         lines = file.readlines()

#     categories = [line.strip() for line in lines if line.strip()]
#     for categori in categories:
#         print(categori)


# def checking_ai_module_api():
#     return

# def checking_recording_module_api():
#     return


# def get_all_devices_from_api():
#     response = requests.request('GET' , recording_url + "devices")
#     response.raise_for_status()
#     data= response.json()
#     return data


# def get_alert_from_ai_module():
#     response = requests.request('GET' , ai_url+ "alerts" )
#     return response.json



