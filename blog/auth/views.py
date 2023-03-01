from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from blog.models import User, db

from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint("auth", __name__)
login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth.login"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).one_or_none()
    if user is None or check_password_hash(user.password, password) == False:
        return render_template("auth/login.html", error=f"Check login information")
    login_user(user)
    return redirect(url_for("user.user_detail", pk=user.id))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("auth/register.html")
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    user = User.query.filter_by(username=username).one_or_none()
    user1 = User.query.filter_by(email=email).one_or_none()
    if user or user1:
        return render_template("auth/register.html", error=f"User with this email or/and username is already registered")
    new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
    )
    db.session.add(new_user)
    db.session.commit()
    return render_template("auth/login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("auth/login.html")


@auth.route("/")
def index():
    return redirect(url_for("article.article_list"))
