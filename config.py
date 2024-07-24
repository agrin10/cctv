import os

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATION = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')
    if not SECRET_KEY:
        if os.environ.get('FLASK_ENV') == 'production':
            raise ValueError("No SECRET_KEY set for Flask application")
        else:
            SECRET_KEY = 'dev'
            print("Warning: Using insecure development SECRET_KEY")

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mysecretpassword@localhost:5432/cctv'

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False