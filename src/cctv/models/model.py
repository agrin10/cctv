from src import db, app
from flask_bcrypt import Bcrypt
import uuid

bcrypt= Bcrypt()

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(225), primary_key=True, nullable=True, unique=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def __repr__(self) -> str:
        return f"the id for the user is {self.id} and the email address is {self.email} and the password is {self.password}"
    
    def set_password(self , password):
        self.password_hash= bcrypt.generate_password_hash(password). decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash , password)
    