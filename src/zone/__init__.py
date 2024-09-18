from flask import Blueprint

zones_bp = Blueprint('zone' , __name__ , template_folder='templates' , static_folder='static')


from src.zone.api_routes import *
from src.zone.web_routes import *