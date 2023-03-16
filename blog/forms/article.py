from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators, SelectMultipleField


class CreateArticleForm(FlaskForm):
    title = StringField("Заголовок", [validators.DataRequired()],)
    body = TextAreaField("Текст", [validators.DataRequired()],)
    tags = SelectMultipleField("Тэги", coerce=int)
    submit = SubmitField("Опубликовать")
