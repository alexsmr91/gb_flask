from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators


class CreateArticleForm(FlaskForm):
    title = StringField("Заголовок", [validators.DataRequired()],)
    body = TextAreaField("Текст", [validators.DataRequired()],)
    submit = SubmitField("Опубликовать")
