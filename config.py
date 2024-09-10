import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATION = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    UPLOAD_EXTENSIONS =os.getenv('UPLOAD_EXTENSIONS')


    # coookies and toke configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_REFRESH_COOKIE_PATH = os.getenv('JWT_REFRESH_COOKIE_PATH')
    JWT_ACCESS_COOKIE_NAME = os.getenv('JWT_ACCESS_COOKIE_NAME')
    JWT_REFRESH_COOKIE_NAME = os.getenv('JWT_REFRESH_COOKIE_NAME')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=6)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_COOKIE_SECURE = False 
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30)
    REMEMBER_COOKIE_DURATION=timedelta(days=7)
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_CSRF_IN_COOKIES = False


    # api urls
    AI_URL = os.getenv('AI_URL')
    RECORDING_URL = os.getenv('RECORDING_URL')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    RTSP_URL = os.getenv('RTSP_URL')


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE=True
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SECURE = False 

