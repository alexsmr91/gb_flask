from flask import Blueprint, render_template

article = Blueprint('article', __name__)


ARTICLES = {
    1: {
        "name": "What is Lorem Ipsum?",
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. "
    },
    2: {
        "name": "Where does it come from?",
        "description": "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. "
    },
    3: {
        "name": "Why do we use it?",
        "description": "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. "
    }
}


@article.route('/')
def article_list():
    return render_template('article/article_list.html', articles=ARTICLES)


@article.route('/<int:pk>')
def article_detail(pk: int):
    return render_template('article/article_detail.html', article=ARTICLES[pk])
