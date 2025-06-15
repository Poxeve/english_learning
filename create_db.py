# Скрипт инициализации базы данных для приложения изучения английского языка
import os
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User, TaskCategory, Task, Solution


def init_database():
    """Инициализация базы данных с начальными данными"""
    app = create_app()
    with app.app_context():
        # Удаляем существующую базу данных
        db_path = os.path.join(app.instance_path, 'app.db')
        if os.path.exists(db_path):
            os.remove(db_path)

        # Создаем все таблицы
        db.create_all()

        # Добавляем начальные данные
        init_sample_data()

        print("✅ База данных успешно инициализирована!")


def init_sample_data():
    """Заполнение базы данных примерами пользователей, категорий и заданий"""
    # Пользователи
    if not User.query.first():
        users = [
            User(username='admin', password_hash=generate_password_hash('admin123'), is_admin=True),
            User(username='student', password_hash=generate_password_hash('student123'))
        ]
        db.session.add_all(users)

    # Категории
    if not TaskCategory.query.first():
        categories = [
            TaskCategory(id=1, name="Present Simple", description="Basic present tense"),
            TaskCategory(id=2, name="Present Continuous", description="Actions happening now"),
            TaskCategory(id=3, name="Past Simple", description="Simple past tense"),
            TaskCategory(id=4, name="Past Continuous", description="Past progressive tense"),
            TaskCategory(id=5, name="Future Simple", description="Simple future tense"),
            TaskCategory(id=6, name="Present Perfect", description="Present perfect tense"),
            TaskCategory(id=7, name="Past Perfect", description="Past perfect tense"),
            TaskCategory(id=8, name="Future Perfect", description="Future perfect tense")
        ]
        db.session.add_all(categories)

    # Задания
    if not Task.query.first():
        tasks = [
            Task(category_id=1, task_number=1, content="Complete the sentence: She ___ (to work) in a bank."),
            Task(category_id=1, task_number=2, content="Make the sentence negative: They play football every Sunday."),
            Task(category_id=2, task_number=1, content="Complete the sentence: Look! It ___ (to rain)."),
            Task(category_id=2, task_number=2, content="Make the sentence negative: They are watching TV now."),
            Task(category_id=3, task_number=1, content="Complete the sentence: Yesterday I ___ (to go) to the cinema."),
            Task(category_id=3, task_number=2, content="Make the sentence negative: She visited her grandmother last week."),
            Task(category_id=4, task_number=1, content="Complete the sentence: While I ___ (to cook) dinner, the phone rang."),
            Task(category_id=4, task_number=2, content="Make the sentence negative: They were playing chess at 5 PM yesterday."),
            Task(category_id=5, task_number=1, content="Complete the sentence: I ___ (to help) you tomorrow."),
            Task(category_id=5, task_number=2, content="Make the sentence negative: They will come to the party."),
            Task(category_id=6, task_number=1, content="Complete the sentence: I ___ (to finish) my homework."),
            Task(category_id=6, task_number=2, content="Make the sentence negative: She has been to Paris."),
            Task(category_id=7, task_number=1, content="Complete the sentence: When I arrived, they ___ (to leave)."),
            Task(category_id=7, task_number=2, content="Make the sentence negative: He had finished the book before dinner."),
            Task(category_id=8, task_number=1, content="Complete the sentence: By next year, I ___ (to graduate)."),
            Task(category_id=8, task_number=2, content="Make the sentence negative: They will have finished the project by Friday.")
        ]
        db.session.add_all(tasks)

    db.session.commit()


if __name__ == '__main__':
    init_database()
