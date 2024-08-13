from src import db 
from flask_bcrypt import Bcrypt
import uuid
from flask_login import UserMixin
from werkzeug.security import check_password_hash , generate_password_hash
from datetime import datetime , timezone
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship



bcrypt = Bcrypt()


class SoftDeleteMixin:
    @declared_attr
    def deleted_at(cls):
        return db.Column(db.DateTime(timezone=True), nullable=True)
    
    @declared_attr
    def is_deleted(cls):
        return db.Column(db.Boolean, default=False, nullable=False)
    
    def soft_delete(self):
        self.deleted_at = datetime.now(timezone.utc)
        self.is_deleted = True

    def restore(self):
        self.deleted_at = None
        self.is_deleted =False


class Users(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.String(225), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    
    def __repr__(self) -> str:
        return f"User(id={self.user_id}, username={self.username})"

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return self.user_id
    

    def toDict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Zone(db.Model, SoftDeleteMixin):
    __tablename__ = "zones"
    
    zone_id = db.Column(db.String(225), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    zone_name = db.Column(db.String(225), nullable=False, unique=True)
    zone_desc = db.Column(db.Text(), nullable=True)

    cameras = db.relationship("Camera", back_populates="zone")
    
    def toDict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class Camera(db.Model, SoftDeleteMixin):
    __tablename__ = 'cameras'

    camera_id = db.Column(db.String(225), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    camera_name = db.Column(db.String(150), nullable=False)
    camera_ip = db.Column(db.String(150), nullable=False, unique=True)
    camera_type = db.Column(db.String(150), nullable=False)
    camera_zone = db.Column(db.String(225), db.ForeignKey("zones.zone_name"), nullable=False)  
    camera_image_path = db.Column(db.String(255), nullable=True)
    
    camera_password_hash = db.Column(db.String(150), nullable=False)
    camera_username = db.Column(db.String(150), nullable=False)

    zone = db.relationship("Zone", back_populates="cameras") 

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def set_password(self, password):
        self.camera_password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.camera_password_hash, password)
    
    
    def toDict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}