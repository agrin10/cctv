from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()  # Correct initialization

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    migrate.init_app(db , app)

    return app

app = create_app()

# from .cctv import models
from src.cctv import models