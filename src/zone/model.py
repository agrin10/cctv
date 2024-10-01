from src import db 
from flask_bcrypt import Bcrypt
import uuid
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

class Zone(db.Model, SoftDeleteMixin):
    __tablename__ = "zones"
    
    # Primary Key should be referenced in the Camera model
    zone_id = db.Column(db.String(225), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    
    # Keep the 'zone_name' unique, but not as a ForeignKey
    zone_name = db.Column(db.String(225), nullable=False, unique=True)
    zone_desc = db.Column(db.Text(), nullable=True)

    # Relationship to 'Camera'
    cameras = db.relationship("Camera", back_populates="zone")    
    
    def toDict(self):
        zone_dict = {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
        
        # Include cameras in the dictionary representation
        zone_dict['cameras'] = [camera.toDict() for camera in self.cameras]
        
        return zone_dict