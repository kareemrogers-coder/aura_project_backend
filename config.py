import os

from flask_sqlalchemy import SQLAlchemy

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'

class TestingConfig:
    pass

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    # JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
    CACHE_TYPE = 'SimpleCache'