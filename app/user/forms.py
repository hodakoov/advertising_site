from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


class LoginForm(FlaskForm):
    username = StringField(
        'Логин',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    remember_me = BooleanField(
        'Запомнить меня',
        default=True,
        render_kw={"class": "form-check-input"}
    )
    submit = SubmitField('Войти', render_kw={"class": "btn btn-primary"})


class RegistrationForm(FlaskForm):
    username = StringField(
        'Логин',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    email = StringField(
        'Электронная почта',
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"}
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    password2 = PasswordField(
        'Повторите пароль',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})


class CreateAdvertisingForm(FlaskForm):
    title = StringField(
        'Название объявления',
        validators=[DataRequired(), Length(2, 100)],
        render_kw={"class": "form-control"}
    )
    description = TextAreaField(
        'Описание товара',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    address = StringField(
        'Адрес',
        validators=[DataRequired(), Length(2, 100)],
        render_kw={"class": "form-control"}
    )
    price = StringField(
        'Цена товара',
        validators=[DataRequired("Поле обязательно для заполнения"),
                    Regexp(regex=r'^\d*$', message="Пожалуйста, введите только цифры")],
        render_kw={"class": "form-control"}
    )
    image = MultipleFileField(
        'Загрузить фотографии объявления',
        validators=[FileAllowed(['png', 'jpg', 'jpeg', 'gif'], message='Пожалуйста, загружайте только картинки')],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField(
        'Отправить',
        render_kw={"class": "form-control btn btn-success"}
    )