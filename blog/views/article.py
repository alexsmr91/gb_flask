import requests
from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound
from blog.models.database import db
from blog.models import Author, Article, Tag
from blog.forms.article import CreateArticleForm


article = Blueprint("articles", __name__)


@article.route("/", endpoint="list")
def articles_list():
    articles = Article.query.all()
    return render_template("article/article_list.html", articles=articles)


@article.route("/api/", endpoint="list_api")
def articles_list_api():
    articles = dict(requests.get('http://127.0.0.1/api/articles/').json())['data']
    print(articles)
    return render_template("article/article_list_api.html", articles=articles)




@article.route("/<int:article_id>/", endpoint="details")
def article_detals(article_id):
    articles = Article.query.filter_by(id=article_id).options(joinedload(Article.tags)).one_or_none()
    if article is None:
        raise NotFound
    return render_template("article/article_detail.html", article=articles)


@article.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
    if request.method == "POST" and form.validate_on_submit():
        articles = Article(title=form.title.data.strip(), body=form.body.data)
        if form.tags.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                articles.tags.append(tag)
        if current_user.author:
            articles.author = current_user.author
        else:
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            articles.author_id = author.id
        db.session.add(articles)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new article!")
            error = "Could not create article!"
        else:
            return redirect(url_for("articles.details", article_id=articles.id))
    return render_template("article/article_create.html", form=form, error=error)
