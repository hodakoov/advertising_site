import os.path
import random
import secrets
import string

from flask import current_app
from flask_login import current_user

from app.show_advertisements.models import Post


def rename_file(pictures):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(pictures)
    new_file_name = random_hex + f_ext
    full_path = os.path.join(current_app.instance_path, current_user.username, 'post_images/')
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    return os.path.join(full_path + new_file_name)


def add_id_ad():
    """
    Создание id для объявления
    """
    random_digits = ''.join(random.sample(string.digits, 10))
    user_id_ad = f'user-{random_digits}'
    while Post.query.filter(Post.ad_id == user_id_ad).first():
        random_digits = ''.join(random.sample(string.digits, 10))
        user_id_ad = f'user-{random_digits}'
    return user_id_ad
