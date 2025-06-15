# Инициализация основного приложения Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Настройка логирования для SQLAlchemy
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Инициализация расширений Flask
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_class=Config):
    # Создание и настройка приложения Flask
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация расширений с приложением
    db.init_app(app)
    login_manager.init_app(app)

    # Настройка Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Регистрация модулей приложения
    from app.main import bp as main_bp
    from app.auth import bp as auth_bp
    from app.admin import bp as admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Инициализация API
    from app.api import api
    api.init_app(app)

    return app


# Импорт моделей в конце для избежания циклических импортов
from app import models