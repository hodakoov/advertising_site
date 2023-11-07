from flask import Flask, flash, redirect, url_for, send_from_directory, render_template
from flask_login import LoginManager

from app.admin.views import blueprint as admin_blueprint
from app.extensions import db
from app.user.models import User
from app.user.views import blueprint as user_blueprint
from app.views import blueprint as index_blueprint
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__, instance_path=Config.UPLOAD_FOLDER)
    app.config.from_object(config_class)
    # Инициализация расширения Flask
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.errorhandler(413)
    def too_large(e):
        flash('Размер файла превышает допустимое значение!', 'danger')
        return redirect(url_for('user.create_ad_user'))

    @app.errorhandler(404)
    def too_large(e):
        return render_template('404_error.html')

    # Регистрация blueprints
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(index_blueprint)
    app.register_blueprint(user_blueprint)

    # Создание БД (при отсутствии)
    with app.app_context():
        db.create_all()

    @app.route('/media/<path:filename>')
    def media(filename):
        return send_from_directory(
            app.instance_path,
            filename,
            as_attachment=True
        )

    return app
