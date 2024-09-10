from flask import Blueprint

camera_bp = Blueprint('camera' , __name__ , template_folder='templates' , static_folder='static')


from .camera_controller import seed_ai_properties
from src.cctv.camera.api_routes import * 
from src.cctv.camera.web_routes import *