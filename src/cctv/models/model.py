from src import db 
from flask_bcrypt import Bcrypt
import uuid
from flask_login import UserMixin
from werkzeug.security import check_password_hash , generate_password_hash


bcrypt = Bcrypt()

class Users(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.String(225), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username})"

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return self.user_id
