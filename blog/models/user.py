from blog.models.database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False, default="", server_default="")
    email = db.Column(db.String(255), unique=True, nullable=False, default="", server_default="")
    name = db.Column(db.String(255), default="", server_default="")
    surname = db.Column(db.String(255), default="", server_default="")
    is_staff = db.Column(db.Boolean, nullable=False, default=False)
    _password = db.Column(db.String(255), nullable=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def validate_password(self, password) -> bool:
        return check_password_hash(self._password, password)

    def __repr__(self):
        return f"<User #{self.id} {self.username!r}>"
