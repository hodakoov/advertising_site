import datetime
import os

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename

from .forms import AddAdvertisingForm
from app.show_advertisements.models import Post
from app.extensions import db
from .utils import rename_file, add_id_ad

blueprint = Blueprint('user_advertisement', __name__, url_prefix='/user_advertisement')


@blueprint.route('/add', methods=['GET', 'POST'])
def add_ad_user():
    if current_user.is_anonymous:
        flash('Для добавления своих объявлений нужно авторизоваться', 'danger')
        return redirect(url_for('user.login'))
    title = 'Страница создания объявления'
    form = AddAdvertisingForm()
    if form.validate_on_submit():
        # Сохранение картинки
        f = form.image.data
        filename = secure_filename(f.filename)
        if filename:
            full_path_image = rename_file(filename)
            f.save(full_path_image)
        else:
            full_path_image = os.path.join(current_app.static_folder, 'images/not_loaded.jpg')

        ad_id = add_id_ad()
        ad_datetime = datetime.datetime.now()
        new_user_ad = Post(
            title=form.title.data,
            description=form.description.data,
            address=form.address.data,
            price=form.price.data,
            image_url=full_path_image,
            ad_id=ad_id,
            ad_datetime=ad_datetime,
            author_id=current_user.id
        )
        db.session.add(new_user_ad)
        db.session.commit()
        flash('Объявление успешно добавлено', 'info')
        return redirect(url_for('index.index'))
    return render_template('user_advertisement/add_ad.html', title=title, form=form)


@blueprint.route('/view')
def view_ad_user():
    if current_user.is_anonymous:
        flash('Для просмотра своих объявлений нужно авторизоваться', 'danger')
        return redirect(url_for('user.login'))
    title = 'Страница отображения своих объявлений'
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(Post.author_id == current_user.id).paginate(page=page, per_page=8)
    return render_template('show_advertisements/index.html', title=title, pagination=pagination)
