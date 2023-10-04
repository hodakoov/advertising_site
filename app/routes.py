from flask import Blueprint, render_template

from app.models.post import Post

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)
