from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_login import  LoginManager 
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
login_manager= LoginManager()
JWT = JWTManager()

def create_app():
    app = Flask(__name__ , template_folder='templates' , static_folder='static' , static_url_path='/')
    app.config.from_object('config.DevelopmentConfig')

    

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    JWT.init_app(app)


    return app


from src.cctv import models
from src.cctv import views