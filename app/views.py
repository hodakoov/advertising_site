from flask import Blueprint, flash, render_template, redirect, request
from flask_login import current_user, login_required
from sqlalchemy import desc

from app.extensions import db
from app.forms import CommentForm
from app.models import Comment, Post
from app.user.models import User
from app.utils import send_comment_notification

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(desc('ad_datetime')).paginate(page=page, per_page=8)
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

        post = Post.query.filter_by(id=form.post_id.data).first()
        comment_author = User.query.filter_by(id=current_user.id).first()

        send_comment_notification(
            post.author.username,
            post.author.email,
            post.title,
            comment_author.username,
            form.comment_text.data
        )
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Некорректный комментарий', 'danger')
    return redirect(request.referrer)
  