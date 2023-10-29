from flask import Blueprint, render_template, request

from app.show_advertisements.models import Post

blueprint = Blueprint('index', __name__)


@blueprint.route('/')
def index():
    title = 'Главная страница'
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(page=page, per_page=8)
    return render_template('show_advertisements/index.html', pagination=pagination, title=title)


@blueprint.route('/<ad_id>')
def detail_ad(ad_id: int):
    post = Post.query.filter_by(ad_id=ad_id).first_or_404()
    images = post.image_url.split(' ')
    return render_template('show_advertisements/detail_page.html', post=post, images=images)
