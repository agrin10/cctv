from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
JWT = JWTManager()


def create_app():
    app = Flask(__name__, template_folder='templates',
                static_folder='static', static_url_path='/')
    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    JWT.init_app(app)

    from src.cctv.users import users_bp
    from src.cctv.camera import camera_bp
    from src.cctv.zone import zones_bp

    app.register_blueprint(camera_bp, url_prefix='/camera')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(zones_bp, url_prefix='/zones')

    return app


from src.cctv.camera.model import Camera
from src.cctv.users.model import Users
