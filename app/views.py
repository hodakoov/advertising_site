from flask import Blueprint, render_template, request
from sqlalchemy import desc

from app.models import Post

blueprint = Blueprint('index', __name__)


@blueprint.route('/')
def index():
    title = 'Главная страница'
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(desc('ad_datetime')).paginate(page=page, per_page=8)
    return render_template('index.html', pagination=pagination, title=title)


@blueprint.route('/<ad_id>')
def detail_ad(ad_id):
    post = Post.query.filter_by(ad_id=ad_id).first_or_404()
    return render_template('detail_page.html', post=post)
