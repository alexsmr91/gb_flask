from flask import Blueprint, render_template
import os


first_start = Blueprint("first_start", __name__)


@first_start.route("/", endpoint="firs_start")
def first_start_view():
    os.system("flask init_db | flask create-admin | flask create-tags")
    return render_template("article/article_list.html")
