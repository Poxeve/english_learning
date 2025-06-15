from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from app.auth import bp
from app import db

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Страница входа в систему"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    """Выход из системы"""
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Страница регистрации"""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)  # Хеширование пароля
        db.session.add(user)  # Добавление пользователя в сессию
        db.session.commit()  # Сохранение изменений в базе данных
        flash('Registration successful!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)