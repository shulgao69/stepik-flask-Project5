from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, DataRequired, EqualTo
from Project5.config import Config

d = Config()
password_length = d.PASSWORD_MIN_LENGTH

class ChangePasswordForm(FlaskForm):
    password = PasswordField("Пароль:", validators=[DataRequired(), Length(min=password_length, message="Пароль должен быть не менее " + str(password_length) +" символов"), EqualTo('confirm_password', message="Пароли не одинаковые")])
    confirm_password = PasswordField("Пароль ещё раз:")


class RegistrationForm(FlaskForm):
    username = StringField("Электропочта", [InputRequired(), Email(message='Проверьте адрес электронной почты')])
    password = PasswordField("Пароль", [InputRequired(),
    Length(min=password_length, message="Пароль должен быть не менее " + str(password_length) +" символов")])


class LoginForm(FlaskForm):
    username = StringField("Электропочта", [InputRequired(), Email(message='Проверьте адрес электронной почты')])
    password = PasswordField("Пароль", [InputRequired(), Length(min=password_length, message="Пароль должен быть не менее " + str(password_length) +" символов")])


class UserOrder(FlaskForm):
    name_user = StringField("Ваше имя", [InputRequired()])
    address_user = StringField("Адрес", [InputRequired()])
    email_user = StringField("Электропочта", [InputRequired()])
    phone_user = StringField("Телефон", [InputRequired()])