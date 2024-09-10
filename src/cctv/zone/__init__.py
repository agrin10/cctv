from flask import Blueprint

zones_bp = Blueprint('zone' , __name__ , template_folder='templates' , static_folder='static')


from src.cctv.zone.api_routes import *
from src.cctv.zone.web_routes import *