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
    db.create_all()
    print("Done!")


@app.cli.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'james'>
    """
    from blog.models import User
    admin = User(username="admin", is_staff=True, password=generate_password_hash("qwe123"), email="a@dm.in")
    james = User(username="james", password="qwe123", email="b@dm.in")
    db.session.add(admin)
    db.session.add(james)
    db.session.commit()
    print("Done! created users:", admin, james)

