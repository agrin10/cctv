from flask import Blueprint

users_bp = Blueprint('users' ,__name__ , template_folder='templates' , static_folder='static')

from src.users.api_routes import *
from src.users.web_routes import *
