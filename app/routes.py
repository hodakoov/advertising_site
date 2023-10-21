from flask import Blueprint, render_template, request

from app.models.post import Post

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
    return render_template('detail_page.html', post=post, images=images)


@bp.route('/add_ad')
def add_ad():
    title = 'Страница создания объявления'
    return render_template('add_ad.html', title=title)
