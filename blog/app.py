from flask import Flask
from blog.config import Config
from blog.article.views import article
from blog.user.views import user
from blog.models import db
from blog.auth import auth
from blog.auth import login_manager


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__, static_folder="static")
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)
    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(article,  url_prefix='/article')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(auth)
