from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import  LoginManager , UserMixin

db = SQLAlchemy()
migrate = Migrate()
login_manager= LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    return app

app = create_app()

from src.cctv import models