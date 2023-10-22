from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import (
    LoginManager, current_user, login_required, login_user, logout_user
)

from app.extensions import db
from app.user.forms import LoginForm, RegistrationForm
from app.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно вошли на сайт', 'info')
            return redirect(url_for('index.index'))

    flash('Неправильные имя или пароль', 'danger')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы разлогинились', 'info')
    return redirect(url_for('index.index'))


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    title = 'Регистрация'
    form = RegistrationForm()
    return render_template('user/registration.html', page_title=title, form=form)


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        if db.session.query(User).filter(User.username == form.username.data).count():
            flash('Пользователь с таким именем уже существует', 'danger')
            return redirect(url_for('user.register'))
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('user.login'))
    flash('Пожалуйста, исправьте ошибки в форме', 'danger')
    return redirect(url_for('user.register'))
