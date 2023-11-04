from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Length, Regexp


class AddAdvertisingForm(FlaskForm):
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

