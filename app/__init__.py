from flask import Flask

from config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация расширения Flask
    db.init_app(app)

    @app.route('/test/')
    def test_page():
        return '<h1> Testing the <p>Flask</p> Application </h1>'

    return app
