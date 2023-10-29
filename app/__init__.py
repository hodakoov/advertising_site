from flask import Flask
from flask_login import LoginManager

from app.show_advertisements.view import blueprint as show_advertisements_blueprint
from app.admin.views import blueprint as admin_blueprint
from app.extensions import db
from app.user_advertisement.view import blueprint as my_advertisement_blueprint
from app.user.models import User
from app.user.views import blueprint as user_blueprint
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация расширения Flask
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Регистрация blueprints
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(show_advertisements_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(my_advertisement_blueprint)

    # Создание БД (при отсутствии)
    with app.app_context():
        db.create_all()

    return app
