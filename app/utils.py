from flask import current_app as app
from flask import request
from urllib.parse import urlparse, urljoin
import requests


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def send_comment_notification(username, email, post_title, comment_author, comment_text):
    domain_name = app.config['EMAIL_SERVICE_DOMAIN_NAME']
    text = f'''
        Пользователь {comment_author} оставил комментарий в объявлении "{post_title}":\n
        {comment_text}
    '''

    return requests.post(
        f'https://api.mailgun.net/v3/{domain_name}/messages',
        auth=('api', app.config['EMAIL_SERVICE_API_KEY']),
        data={
            'from': f'Клон Авито <postmaster@{domain_name}>',
            'to': f'{username} <{email}>',
            'subject': f'Новый комментарий в объявлении {post_title}',
            'text': text
        }
    )
