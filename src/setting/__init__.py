from flask import Blueprint

setting_bp = Blueprint('setting' ,__name__ , template_folder='templates' , static_folder='static')

from src.setting.api_routes import *
from src.setting.web_routes import *
