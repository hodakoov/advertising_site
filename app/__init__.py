from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required

from app import routes
from app.admin.views import blueprint as admin_blueprint
from app.extensions import db
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
    app.register_blueprint(routes.bp)
    app.register_blueprint(user_blueprint)

    # Создание БД (при отсутствии)
    with app.app_context():
        db.create_all()

    return app
