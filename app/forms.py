from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from app.models.post import Post


class CommentForm(FlaskForm):
    post_id = HiddenField('ID объявления', validators=[DataRequired()])
    comment_text = StringField(
        'Добавить комментарий:',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})

    def validate_post_id(self, post_id):
        if not Post.query.get(post_id.data):
            raise ValidationError('Объявления с таким id нет')
