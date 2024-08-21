import os
from datetime import timedelta

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATION = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')
    UPLOAD_FOLDER = 'src/static/uploads'
    UPLOAD_EXTENSIONS = [".jpg", ".png"]



    if not SECRET_KEY:
        if os.environ.get('FLASK_ENV') == 'production':
            raise ValueError("No SECRET_KEY set for Flask application")
        else:
            SECRET_KEY = 'dev'
            print("Warning: Using insecure development SECRET_KEY")

    # coookies and toke configuration
    JWT_SECRET_KEY = 'tokensecrtkey'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False 
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/api/refresh'
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30)
    REMEMBER_COOKIE_DURATION=timedelta(days=7)
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_CSRF_IN_COOKIES = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mysecretpassword@localhost:5432/cctv'
    RTSP_URL = os.getenv(
        'RTSP_URL', 'rtsp://admin:admin123@192.168.10.247:554/cam/realmonitor?channel=1&subtype=1')


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE=True
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SECURE = False 

