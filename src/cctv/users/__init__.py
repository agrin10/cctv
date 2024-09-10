from flask import Blueprint

users_bp = Blueprint('users' ,__name__ , template_folder='templates' , static_folder='static')

# from src.cctv.users.api_routes import *
# from src.cctv.users.web_routes import *
