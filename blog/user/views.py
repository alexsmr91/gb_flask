from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from blog.models import User

user = Blueprint('user', __name__)




@user.route('/')
def user_list():
    users = User.query.all()
    print(users[0].id)
    return render_template('user/user_list.html', users=users)


@user.route('/<int:pk>')
def user_detail(pk: int):
    one_user = User.query.filter_by(id=pk).one_or_none()
    if one_user is None:
        raise NotFound(f"User #{pk} doesn't exist!")
    return render_template('user/user_detail.html', user=one_user)
