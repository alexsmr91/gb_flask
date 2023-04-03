import os
from blog.models.database import db
from flask import Blueprint, render_template

commands = Blueprint('commands', __name__)


@commands.cli.command('init-db')
def _init_db():
    init_db()


@commands.cli.command("create-admin")
def _create_admin():
    create_admin()


@commands.cli.command("create-tags")
def _create_tags():
    create_tags()


def init_db():
    """
    Run in your terminal:
    flask init-db
    """
    try:
        db.create_all()
        print("Init DB: Done!")
    except Exception as error:
        print(error)


def create_admin():
    """
    Run in your terminal:
    ➜ flask create-admin
    > created admin: <User #1 'admin'>
    """
    from blog.models import User
    admin = User(username="admin", is_staff=True)
    admin.password = os.environ.get("ADMIN_PASSWORD") or "qwe123"
    try:
        db.session.add(admin)
        db.session.commit()
        print("created admin:", admin)
    except Exception as error:
        print(error)


def create_tags():
    """
    Run in your terminal:
    ➜ flask create-tags
    """
    from blog.models import Tag
    for name in ["flask", "django", "python", "sqlalchemy", "news"]:
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
    print("created tags")


@commands.route("/", endpoint="first_start")
def first_start():
    first = os.environ.get("FIRST", True)
    if first:
        init_db()
        create_admin()
        create_tags()
        os.environ.setdefault("FIRST", "0")
    return render_template("authors/list.html")
