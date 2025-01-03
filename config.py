import os

from flask_sqlalchemy import SQLAlchemy

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'

class TestingConfig:
    pass

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_SQLALCHEMY_DATABASE_URI')
    CACHE_TYPE = 'SimpleCache'