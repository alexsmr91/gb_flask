from flask import Flask

from blog.article.views import article
from blog.user.views import user


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static")
    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(article,  url_prefix='/article')
    app.register_blueprint(user, url_prefix='/user')
