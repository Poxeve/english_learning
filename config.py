# Настройки конфигурации приложения
import os
from dotenv import load_dotenv
from pathlib import Path

# Загрузка переменных окружения из файла .env
load_dotenv()

# Настройка базовых директорий
basedir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(basedir, 'instance')
os.makedirs(instance_dir, exist_ok=True)


class Config:
    """Базовый класс конфигурации с общими настройками"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(instance_dir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Логирование SQL запросов (False в продакшене)

    # Настройки Flask-Login
    REMEMBER_COOKIE_DURATION = 3600
    SESSION_PROTECTION = 'strong'

    @staticmethod
    def init_app(app):
        """Инициализация конфига для приложения"""
        if not os.path.exists(instance_dir):
            os.makedirs(instance_dir, exist_ok=True)


class DevelopmentConfig(Config):
    """Конфигурация для среды разработки"""
    DEBUG = False
    SQLALCHEMY_ECHO = False  # Показывать SQL запросы в консоли


class TestingConfig(Config):
    """Конфигурация для тестовой среды"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Конфигурация для продакшн среды"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Словарь конфигураций для разных окружений
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'test': TestConfig,
    'default': DevelopmentConfig
}
