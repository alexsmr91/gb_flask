from flask import Flask
from blog.config import BaseConfig, DevConfig, TestingConfig
from blog.article.views import article
from blog.user.views import user
from blog.models import db
from blog.auth import auth
from blog.auth import login_manager
from flask_migrate import Migrate



def create_app(config_class=DevConfig) -> Flask:
    app = Flask(__name__, static_folder="static")
    app.config.from_object(config_class)
    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)
    login_manager.init_app(app)
    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(article,  url_prefix='/article')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(auth)
