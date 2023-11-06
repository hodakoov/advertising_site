from flask import current_app as app
from flask import render_template
import requests


def send_comment_notification(username, email, post_title, comment_author, comment_text):
    domain_name = app.config['EMAIL_SERVICE_DOMAIN_NAME']
    text = f'''
        Пользователь {comment_author} оставил комментарий в объявлении "{post_title}":\n
        {comment_text}
    '''
    html = render_template(
        'email_notification.html',
        comment_author=comment_author,
        post_title=post_title,
        comment_text=comment_text
    )

    return requests.post(
        f'https://api.mailgun.net/v3/{domain_name}/messages',
        auth=('api', app.config['EMAIL_SERVICE_API_KEY']),
        data={
            'from': f'Клон Авито <postmaster@{domain_name}>',
            'to': f'{username} <{email}>',
            'subject': f'Новый комментарий в объявлении {post_title}',
            'text': text,
            'html': html
        }
    )
