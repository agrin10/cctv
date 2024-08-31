from src.cctv.models.model import Users, db , Zone , Camera
from src import app
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_jwt_identity, get_csrf_token
from flask import jsonify , make_response
import cv2
import pytz
import requests


ai_url = app.config['AI_URL']
recording_url = app.config['RECORDING_URL']


def api_get_devices():
    url = ai_url+"/devices"
    response = requests.get(url)
    return response.json()