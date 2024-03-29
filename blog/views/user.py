from flask import Blueprint, render_template
from werkzeug.exceptions import Unauthorized
from flask_login import login_required, current_user
from blog.models import User

users = Blueprint('users', __name__)


@users.route('/')
@login_required
def user_list():
    if current_user.is_staff:
        data = User.query.all()
        return render_template('user/user_list.html', users=data)
    else:
        return user_detail(current_user.id)


@users.route('/<int:pk>')
@login_required
def user_detail(pk: int):
    one_user = None
    if pk == current_user.id or current_user.is_staff:
        one_user = User.query.filter_by(id=pk).one_or_none()
    if one_user is None:
        raise Unauthorized(f"User #{pk} doesn't exist!")
    return render_template('user/user_detail.html', user=one_user)
