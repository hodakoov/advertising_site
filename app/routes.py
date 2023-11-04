from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import CommentForm
from app.models.comment import Comment
from app.models.post import Post
from app.utils import get_redirect_target

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(page=page, per_page=8)
    return render_template('index.html', pagination=pagination)


@bp.route('/<ad_id>')
def detail_ad(ad_id: int):
    post = Post.query.filter_by(ad_id=ad_id).first_or_404()
    images = post.image_url.split(' ')
    comment_form = CommentForm(post_id=post.id)
    return render_template(
        'detail_page.html', post=post, images=images, comment_form=comment_form
    )


@bp.route('/comment', methods=['POST'])
@login_required
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            text=form.comment_text.data,
            post_id=form.post_id.data,
            author_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий добавлен', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    'Ошибка в поле {}: {}'.format(
                        getattr(form, field).label.text, error
                    )
                )
    return redirect(get_redirect_target())
