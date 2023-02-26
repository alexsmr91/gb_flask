from flask import Blueprint, render_template

user = Blueprint('user', __name__)


USERS = {
    1: {
        "name": "Alex",
        "surname": "Di"
    },
    2: {
        "name": "Pavel",
        "surname": "Pi"
    },
    3: {
        "name": "Ivan",
        "surname": "Li"
    }
}


@user.route('/')
def user_list():
    return render_template('user/user_list.html', users=USERS)


@user.route('/<int:pk>')
def user_detail(pk: int):
    return render_template('user/user_detail.html', user=USERS[pk])
