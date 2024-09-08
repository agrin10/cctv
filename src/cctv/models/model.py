from src import db 
from flask_bcrypt import Bcrypt
import uuid
from flask_login import UserMixin
from werkzeug.security import check_password_hash , generate_password_hash
from datetime import datetime , timezone
from sqlalchemy.ext.declarative import declared_attr



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
        zone_dict = {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
        
        zone_dict['cameras'] = [camera.toDict() for camera in self.cameras]
        
        return zone_dict
    

# Association Table
camera_ai_relationship = db.Table('camera_ai',
    db.Column('camera_id', db.String(225), db.ForeignKey('cameras.camera_id'), primary_key=True),
    db.Column('ai_property_id', db.String(225), db.ForeignKey('ai_properties.id'), primary_key=True)
)

camera_ai_relationship = db.Table('camera_ai_relationship',
    db.Column('camera_id', db.String(225), db.ForeignKey('cameras.camera_id'), primary_key=True),
    db.Column('ai_property_id', db.String(225), db.ForeignKey('ai_properties.id'), primary_key=True)
)

class Camera(db.Model):
    __tablename__ = 'cameras'

    camera_id = db.Column(db.String(225), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    camera_name = db.Column(db.String(150), nullable=False)
    camera_ip = db.Column(db.String(150), nullable=False, unique=True)
    camera_type = db.Column(db.String(150), nullable=False)
    camera_zone = db.Column(db.String(225), db.ForeignKey("zones.zone_name"), nullable=False)  
    camera_image_path = db.Column(db.String(255), nullable=True)
    camera_record = db.Column(db.Boolean, default=False)
    camera_password = db.Column(db.String(150), nullable=False)
    camera_username = db.Column(db.String(150), nullable=False)
    camera_port = db.Column(db.Integer, nullable=True)

    zone = db.relationship("Zone", back_populates="cameras") 
    ai_properties = db.relationship("AiProperties", secondary=camera_ai_relationship, back_populates="cameras")

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def toDict(self):
        camera_dict = {
            "camera_id": str(self.camera_id),
            "camera_name": self.camera_name,
            "camera_ip": self.camera_ip,
            "camera_type": self.camera_type,
            "camera_zone": self.camera_zone,
            "camera_image_path": self.camera_image_path,
            "camera_record": str(self.camera_record),
            "camera_password": self.camera_password,
            "camera_username": self.camera_username,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "deleted_at": str(getattr(self, 'deleted_at', None)),  
            "is_deleted": str(getattr(self, 'is_deleted', False)), 
        }

        # Zone information
        if self.zone:
            camera_dict['zone'] = {
                "zone_id": str(self.zone.zone_id),
                "zone_name": self.zone.zone_name
            }
        else:
            camera_dict['zone'] = None

        camera_dict['ai_properties'] = [ai_property.name for ai_property in self.ai_properties]

        return camera_dict
        

class AiProperties(db.Model):
    __tablename__ = 'ai_properties'
    
    id = db.Column(db.String(225), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(250), unique=False, nullable=False)
    label = db.Column(db.String(250))

    # Remove camera_id since this is a many-to-many relationship
    cameras = db.relationship("Camera", secondary=camera_ai_relationship, back_populates="ai_properties")

    def toDict(self):
        return {
            'property_id': self.id,
            'name': self.name,
            'label': self.label
        }