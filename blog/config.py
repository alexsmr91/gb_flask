import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    TESTING = os.environ.get("TESTING", False)
    DEBUG = os.environ.get("DEBUG", False)
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    WTF_CSRF_ENABLED = True
    FLASK_ADMIN_SWATCH = 'cosmo'


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///../blog/db.sqlite"
    SECRET_KEY = os.environ.get("SECRET_KEY", "111111111111111111111111")


class TestingConfig(BaseConfig):
    TESTING = True
