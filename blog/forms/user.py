from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField


class UserBaseForm(FlaskForm):
    name = StringField("Имя")
    surname = StringField("Фамилия")
    username = StringField("Имя пользователя", [validators.DataRequired()],)
    email = StringField("Электронная почта",
                        [
                            validators.DataRequired(),
                            validators.Email(),
                            validators.Length(min=6, max=200),
                        ],
                        filters=[lambda data: data and data.lower()],)


class RegistrationForm(UserBaseForm):
    password = PasswordField("Новый пароль",
                             [
                                 validators.DataRequired(),
                                 validators.EqualTo("confirm", message="Пароли должны совпадать"),
                             ],)
    confirm = PasswordField("Повторите пароль")
    submit = SubmitField("Зарегистрироваться")


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", [validators.DataRequired()],)
    password = PasswordField("Пароль", [validators.DataRequired()],)
    submit = SubmitField("Войти")
