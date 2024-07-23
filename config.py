class Config:
    DEBUG= False
    TESTTING= False
    SQLALCHEMY_TRACK_MODIFICATIONS= False

class DevelopmentConfig(Config):
    DEBUG   = True
    SQLALCHEMY_DATABASE_URI= 'postgresql://postgres:mysecretpassword@localhost:5432/cctv'

class TestingConfig(Config):
    TESTTING=True

class ProductionConfig(Config):
    DEBUG = False
    