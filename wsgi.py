from blog.app import create_app
from blog.models.database import db
from werkzeug.security import generate_password_hash


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


@app.cli.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'user'>
    """
    from blog.models import User
    admin = User(username="admin", is_staff=True, password=generate_password_hash("qwe123"), email="a@dm.in")
    user = User(username="user", password=generate_password_hash("qwe123"), email="b@dm.in")
    try:
        db.session.add(admin)
        db.session.add(user)
        db.session.commit()
        print("Done! created users:", admin, user)
    except Exception as error:
        print(error)

