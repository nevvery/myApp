import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Config:
    BASE_DIR = BASE_DIR
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_LOGIN_URL = '/auth/login'
    SECURITY_POST_LOGIN_VIEW = '/main/index'
    SECURITY_POST_LOGOUT_VIEW = '/auth/login'
    SECURITY_REGISTERABLE = False
    SESSION_COOKIE_SAMESITE = 'Strict'
    REMEMBER_COOKIE_SAMESITE = 'Strict'
    TESTING = False


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    TESTING = True
