from flask import Blueprint

camera_bp = Blueprint('camera' , __name__ , template_folder='templates' , static_folder='static')


from src.camera.api_routes import * 
from src.camera.web_routes import *