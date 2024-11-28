# src/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from importlib import import_module


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
JWT = JWTManager()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    JWT.init_app(app)

    
    
    from src.users.seeder import seed_user_management
    from src.camera.seeder import seed_ai_properties
    with app.app_context():
        db.create_all()  
        seed_user_management()  
        seed_ai_properties()

    register_blueprint(app)

    return app


from importlib import import_module

def register_blueprint(app):
    url_prefixes = {
        'camera': '/camera',
        'zone': '/zones',
        'users': '/users',
        'setting': '/setting',
        'web': None
    }

    modules = ('camera', 'zone', 'users', 'setting', 'web')

    for module in modules:
        # Import the shared Blueprint from each module's __init__.py or blueprint.py
        blueprint_module = import_module(f'src.{module}') 
        blueprint_name = f'{module}_bp' 

        # Import both web_routes and api_routes so that routes are registered to the Blueprint
        import_module(f'src.{module}.web_routes')  
        import_module(f'src.{module}.api_routes')  

        # Register the shared blueprint to the app with the appropriate URL prefix
        app.register_blueprint(getattr(blueprint_module, blueprint_name), url_prefix=url_prefixes[module])


from src.zone.model import Zone 
from src.camera.model import Camera 
from src.users.model import Users 
