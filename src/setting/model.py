from src import db , login_manager
from flask_bcrypt import Bcrypt
import uuid
from flask_login import UserMixin
from datetime import datetime , timezone
from sqlalchemy.ext.declarative import declared_attr

