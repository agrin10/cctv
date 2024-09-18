from flask import Blueprint

camera_bp = Blueprint('camera' , __name__ , template_folder='templates' , static_folder='static')


from src.cctv.camera.api_routes import * 
from src.cctv.camera.web_routes import *