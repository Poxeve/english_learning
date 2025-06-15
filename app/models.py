# Модели базы данных для приложения изучения английского языка
from datetime import datetime
from pytz import UTC
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    """Модель пользователя для аутентификации и управления пользователями"""
    __tablename__ = 'users'  # Единое имя таблицы

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class TaskCategory(db.Model):
    """Модель для организации заданий по категориям"""
    __tablename__ = 'task_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(300))
    tasks = db.relationship('Task', backref='category', lazy=True)


class Task(db.Model):
    """Модель для хранения заданий по английскому языку"""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('task_categories.id'), nullable=False)
    task_number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

    def get_full_id(self):
        """Генерирует полный ID задачи в формате 'категория_номер'"""
        return f"{self.category_id:02d}{self.task_number:02d}"


class Solution(db.Model):
    """Модель для хранения решений пользователей"""
    __tablename__ = 'solutions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    content = db.Column(db.Text)
    feedback = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    reviewed_at = db.Column(db.DateTime)
    is_reviewed = db.Column(db.Boolean, default=False)

    task = db.relationship('Task', backref='solutions')
    user = db.relationship('User', backref='solutions')