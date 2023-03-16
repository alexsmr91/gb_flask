from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from blog.models import User, db
from sqlalchemy.exc import IntegrityError
from blog.forms.user import RegistrationForm, LoginForm

auth = Blueprint("auth", __name__)
login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth.login"))


@auth.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated and not current_user.is_staff:
        return redirect(url_for("auth.index"))
    error = None
    form = LoginForm(request.form)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).one_or_none()
        if user is None or not user.validate_password(password):
            return render_template("auth/login.html", form=form, error=f"Check login information")
        login_user(user)
        return redirect(url_for("user.user_detail", pk=user.id))
    return render_template("auth/login.html", form=form, error=error)


@auth.route("/register/", methods=["GET", "POST"], endpoint="register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("auth.index"))
    error = None
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).count():
            form.username.errors.append("username already exists!")
            return render_template("auth/register.html", form=form)
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("email already exists!")
            return render_template("auth/register.html", form=form)
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            username=form.username.data,
            email=form.email.data,
            is_staff=False,
        )
        user.password = form.password.data
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create user!")
            error = "Could not create user!"
        else:
            current_app.logger.info("Created user %s", user)
            login_user(user)
            return redirect(url_for("auth.index"))
    return render_template("auth/register.html", form=form, error=error)


@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/")
def index():
    return redirect(url_for("article.article_list"))
