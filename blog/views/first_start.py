from flask import Blueprint, render_template

from wsgi import init_db, create_admin, create_tags

first_start = Blueprint("first_start", __name__)


@first_start.route("/", endpoint="firs_start")
def first_start():
    init_db()
    create_admin()
    create_tags()
    return render_template("article/article_list.html")
