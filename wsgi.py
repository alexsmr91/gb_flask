import os
from blog.app import create_app
from blog.models.database import db


app = create_app()


@app.cli.command("init-db")
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


@app.cli.command("create-admin")
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


@app.cli.command("create-tags")
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


FIRST = os.environ.get("FIRST", False)

if FIRST:
    init_db()
    create_admin()
    create_tags()
    os.environ.setdefault("FIRST", "0")
