import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///dev_database.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///:memory:'
    UPLOAD_FOLDER = 'test_uploads'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///prod_database.db'
