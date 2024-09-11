from flask import Blueprint

setting_bp = Blueprint('setting' ,__name__ , template_folder='templates' , static_folder='static')

from src.cctv.setting.api_routes import *
from src.cctv.setting.web_routes import *
