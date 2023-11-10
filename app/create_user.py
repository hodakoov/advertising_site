from getpass import getpass
import sys

from app import create_app
from app.user.models import db, User

app = create_app()

with app.app_context():
    username = input('Введите имя:\n')
    if User.query.filter(User.username == username).count():
        print('Пользователь с таким именем уже есть')
        sys.exit(0)

    password1 = getpass('Введите пароль:\n')
    password2 = getpass('Повторите ввод:\n')
    if not password1 == password2:
        print('Пароли не совпадают')
        sys.exit(0)

    is_admin = input('Сделать нового пользователя админом? (y/n)\n')
    role = 'admin' if is_admin[0].lower() == 'y' else 'user'

    new_user = User(username=username, role=role)
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print('Создан пользователь с id={}'.format(new_user.id))
