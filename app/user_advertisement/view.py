import datetime
import os

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from .forms import AddAdvertisingForm
from app.show_advertisements.models import Post
from app.extensions import db
from .utils import rename_file, add_id_ad

blueprint = Blueprint('user_advertisement', __name__)


@blueprint.route('/add', methods=['GET', 'POST'])
def add_ad_user():
    if current_user.is_anonymous:
        flash('Для добавления своих объявлений нужно авторизоваться', 'warning')
        return redirect(url_for('user.login'))
    title = 'Страница создания объявления'
    form = AddAdvertisingForm()
    if form.validate_on_submit():
        # Сохранение картинки
        f = form.image.data
        filename = secure_filename(f.filename)
        if filename:
            path_image, full_path_image = rename_file(filename)
            path_image = path_image[0]
            f.save(full_path_image[0])
        else:
            path_image = 'images/not_loaded.jpg'
            # # Сохранение картинки
            # data = form.image.data
            # list_path_image = []
            # if data[0].filename == '':
            #     path_image = 'images/not_loaded.jpg'
            #     list_path_image.append(path_image)
            # else:
            #     for f in data:
            #         filename = secure_filename(f.filename)
            #         path_image, full_path_image = rename_file(filename)
            #         path_image = path_image[0]
            #         f.save(full_path_image[0])
            #         list_path_image.append(path_image)

        ad_id = add_id_ad()
        ad_datetime = datetime.datetime.now()
        new_user_ad = Post(
            title=form.title.data,
            description=form.description.data,
            address=form.address.data,
            price=form.price.data,
            image_url=path_image,
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
        flash('Для просмотра своих объявлений нужно авторизоваться', 'warning')
        return redirect(url_for('user.login'))
    title = 'Страница отображения своих объявлений'
    page = request.args.get('page', 1, type=int)
    pagination = Post.query\
        .filter(Post.author_id == current_user.id)\
        .order_by(desc('ad_datetime'))\
        .paginate(page=page, per_page=8)
    return render_template('user_advertisement/view_ad.html', title=title, pagination=pagination)


@blueprint.route('/update/<ad_id>', methods=['GET', 'POST'])
def update_ad_user(ad_id):
    if current_user.is_anonymous:
        flash('Для редактирования своих объявлений нужно авторизоваться', 'warning')
        return redirect(url_for('user.login'))

    post = Post.query.filter(Post.ad_id == ad_id).first()
    if current_user.id != post.author_id:
        flash('У вас нет прав на изменения этого объявления', 'danger')
        return redirect(url_for('index.index'))

    title = 'Страница редактирования объявления'
    form = AddAdvertisingForm(obj=post)
    if form.validate_on_submit():
        # Обновление картинки
        f = form.image.data
        filename = secure_filename(f.filename)
        if filename:
            full_path_image = rename_file(filename)
            f.save(full_path_image)
        else:
            full_path_image = post.image_url
        post.image_url = full_path_image

        form.populate_obj(post)
        db.session.commit()
        flash('Объявление успешно обновлено', 'info')
        return redirect(url_for('index.detail_ad', ad_id=post.ad_id))
    return render_template('user_advertisement/add_ad.html', title=title, form=form)


@blueprint.route('/delete/<ad_id>')
def delete_ad_user(ad_id):
    if current_user.is_anonymous:
        flash('Для удаления своих объявлений нужно авторизоваться', 'warning')
        return redirect(url_for('user.login'))

    post = Post.query.filter(Post.ad_id == ad_id).first()
    if current_user.id != post.author_id:
        flash('У вас нет прав для удаления этого объявления', 'danger')
        return redirect(url_for('index.index'))

    db.session.delete(post)
    db.session.commit()
    flash('Объявление успешно удалено', 'info')
    return redirect(url_for('user_advertisement.view_ad_user'))
