from flask import Flask

from config import Config
from app.extensions import db
from app import routes


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация расширения Flask
    db.init_app(app)

    # Регистрация blueprints
    app.register_blueprint(routes.bp)

    # Создание БД (при отсутствии)
    with app.app_context():
        db.create_all()

    return app
