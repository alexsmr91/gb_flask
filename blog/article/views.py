from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from blog.models.database import db
from blog.models import Author, Article
from blog.forms.article import CreateArticleForm


article = Blueprint("articles", __name__)


@article.route("/", endpoint="list")
def articles_list():
    articles = Article.query.all()
    return render_template("article/article_list.html", articles=articles)


@article.route("/<int:article_id>/", endpoint="details")
def article_detals(article_id):
    articles = Article.query.filter_by(id=article_id).one_or_none()
    if article is None:
        raise NotFound
    return render_template("article/article_detail.html", article=articles)


@article.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        articles = Article(title=form.title.data.strip(), body=form.body.data)
        db.session.add(articles)
        if current_user.author:
            # use existing author if present
            articles.author = current_user.author
        else:
            # otherwise create author record
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            articles.author = author.id
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new article!")
            error = "Could not create article!"
        else:
            return redirect(url_for("articles.details", article_id=articles.id))
    return render_template("article/article_create.html", form=form, error=error)
