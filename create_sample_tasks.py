# Скрипт создания примеров заданий для приложения изучения английского языка
from app import create_app, db
from app.models import User, TaskCategory, Task
from werkzeug.security import generate_password_hash
import os
from pathlib import Path
from sqlalchemy.exc import IntegrityError


def init_db():
    """Инициализация базы данных с примерами заданий и категорий"""
    app = create_app()
    with app.app_context():
        print("Начинаем инициализацию базы данных...")

        # Удаление существующих баз данных
        instance_path = Path(app.instance_path)
        app_db_path = instance_path / 'app.db'
        users_db_path = instance_path / 'users.db'

        print("Удаляем старые файлы баз данных...")
        for db_file in [app_db_path, users_db_path]:
            if db_file.exists():
                db_file.unlink()
                print(f"   Удален файл: {db_file}")

        # Создание папки instance если ее нет
        instance_path.mkdir(parents=True, exist_ok=True)

        # Создание таблиц
        print("Создаем структуру базы данных...")
        try:
            db.create_all()
            print("Таблицы созданы")

            # Добавление пользователей (в users.db)
            print("Добавляем пользователей...")
            users_data = [
                {'username': 'admin', 'password': 'admin123', 'is_admin': True},
                {'username': 'student', 'password': 'student123', 'is_admin': False}
            ]

            for user_data in users_data:
                try:
                    user = User(
                        username=user_data['username'],
                        password_hash=generate_password_hash(user_data['password']),
                        is_admin=user_data['is_admin']
                    )
                    db.session.add(user)
                    db.session.commit()
                    print(f"Пользователь {user_data['username']} добавлен")
                except IntegrityError:
                    db.session.rollback()
                    print(f"Пользователь {user_data['username']} уже существует")

            # Добавление категории (в app.db)
            print("Добавляем категории...")
            categories_data = [
                {'id': 1, 'name': 'Present Simple', 'description': 'Используется для описания регулярных действий, фактов и общих истин'},
                {'id': 2, 'name': 'Present Continuous', 'description': 'Используется для описания действий, происходящих в момент речи'},
                {'id': 3, 'name': 'Present Perfect', 'description': 'Используется для описания действий, которые произошли в прошлом, но имеют связь с настоящим'},
                {'id': 4, 'name': 'Present Perfect Continuous', 'description': 'Используется для описания действий, которые начались в прошлом и продолжаются до настоящего момента'},
                {'id': 5, 'name': 'Past Simple', 'description': 'Используется для описания завершенных действий в прошлом'},
                {'id': 6, 'name': 'Past Continuous', 'description': 'Используется для описания действий, происходивших в определенный момент в прошлом'},
                {'id': 7, 'name': 'Past Perfect', 'description': 'Используется для описания действий, которые произошли до определенного момента в прошлом'},
                {'id': 8, 'name': 'Past Perfect Continuous', 'description': 'Используется для описания действий, которые происходили до определенного момента в прошлом'},
                {'id': 9, 'name': 'Future Simple', 'description': 'Используется для описания действий, которые произойдут в будущем'},
                {'id': 10, 'name': 'Future Continuous', 'description': 'Используется для описания действий, которые будут происходить в определенный момент в будущем'},
                {'id': 11, 'name': 'Future Perfect', 'description': 'Используется для описания действий, которые завершатся к определенному моменту в будущем'},
                {'id': 12, 'name': 'Future Perfect Continuous', 'description': 'Используется для описания действий, которые будут происходить до определенного момента в будущем'}
            ]

            for cat_data in categories_data:
                try:
                    category = TaskCategory(**cat_data)
                    db.session.add(category)
                    db.session.commit()
                    print(f"Категория {cat_data['name']} добавлена")
                except IntegrityError:
                    db.session.rollback()
                    print(f"Категория {cat_data['name']} уже существует")

            # Добавление задач (в app.db)
            print("Добавляем задачи...")
            tasks_data = [
                # Present Simple
                {'category_id': 1, 'task_number': 1, 'content': "Complete the sentence: She ___ (work) in a bank."},
                {'category_id': 1, 'task_number': 2, 'content': "Make the sentence negative: They go to school every day."},
                {'category_id': 1, 'task_number': 3, 'content': "Ask a question: He plays tennis on weekends."},
                
                # Present Continuous
                {'category_id': 2, 'task_number': 1, 'content': "Complete the sentence: Look! It ___ (rain) outside."},
                {'category_id': 2, 'task_number': 2, 'content': "Make the sentence negative: They are watching TV now."},
                {'category_id': 2, 'task_number': 3, 'content': "Ask a question: She is cooking dinner."},
                
                # Present Perfect
                {'category_id': 3, 'task_number': 1, 'content': "Complete the sentence: I ___ (never/be) to Paris."},
                {'category_id': 3, 'task_number': 2, 'content': "Make the sentence negative: They have finished their homework."},
                {'category_id': 3, 'task_number': 3, 'content': "Ask a question: She has visited London twice."},
                
                # Present Perfect Continuous
                {'category_id': 4, 'task_number': 1, 'content': "Complete the sentence: She ___ (study) English for 5 years."},
                {'category_id': 4, 'task_number': 2, 'content': "Make the sentence negative: They have been waiting for an hour."},
                {'category_id': 4, 'task_number': 3, 'content': "Ask a question: He has been working here since 2010."},
                
                # Past Simple
                {'category_id': 5, 'task_number': 1, 'content': "Complete the sentence: Yesterday, I ___ (go) to the cinema."},
                {'category_id': 5, 'task_number': 2, 'content': "Make the sentence negative: They visited their grandparents last week."},
                {'category_id': 5, 'task_number': 3, 'content': "Ask a question: She bought a new car."},
                
                # Past Continuous
                {'category_id': 6, 'task_number': 1, 'content': "Complete the sentence: At 8 PM yesterday, I ___ (watch) TV."},
                {'category_id': 6, 'task_number': 2, 'content': "Make the sentence negative: They were playing football when it started to rain."},
                {'category_id': 6, 'task_number': 3, 'content': "Ask a question: She was cooking dinner when I called."},
                
                # Past Perfect
                {'category_id': 7, 'task_number': 1, 'content': "Complete the sentence: By the time we arrived, the movie ___ (already/start)."},
                {'category_id': 7, 'task_number': 2, 'content': "Make the sentence negative: They had finished their work before lunch."},
                {'category_id': 7, 'task_number': 3, 'content': "Ask a question: She had left before I got there."},
                
                # Past Perfect Continuous
                {'category_id': 8, 'task_number': 1, 'content': "Complete the sentence: She ___ (study) for 3 hours when I called."},
                {'category_id': 8, 'task_number': 2, 'content': "Make the sentence negative: They had been waiting for an hour when the bus arrived."},
                {'category_id': 8, 'task_number': 3, 'content': "Ask a question: He had been working there for 5 years."},
                
                # Future Simple
                {'category_id': 9, 'task_number': 1, 'content': "Complete the sentence: Tomorrow, I ___ (go) to the beach."},
                {'category_id': 9, 'task_number': 2, 'content': "Make the sentence negative: They will visit us next week."},
                {'category_id': 9, 'task_number': 3, 'content': "Ask a question: She will start her new job next month."},
                
                # Future Continuous
                {'category_id': 10, 'task_number': 1, 'content': "Complete the sentence: At 8 PM tomorrow, I ___ (watch) a movie."},
                {'category_id': 10, 'task_number': 2, 'content': "Make the sentence negative: They will be playing tennis at this time tomorrow."},
                {'category_id': 10, 'task_number': 3, 'content': "Ask a question: She will be cooking dinner when we arrive."},
                
                # Future Perfect
                {'category_id': 11, 'task_number': 1, 'content': "Complete the sentence: By next year, I ___ (finish) my studies."},
                {'category_id': 11, 'task_number': 2, 'content': "Make the sentence negative: They will have completed the project by Friday."},
                {'category_id': 11, 'task_number': 3, 'content': "Ask a question: She will have arrived by 6 PM."},
                
                # Future Perfect Continuous
                {'category_id': 12, 'task_number': 1, 'content': "Complete the sentence: By next month, I ___ (work) here for 5 years."},
                {'category_id': 12, 'task_number': 2, 'content': "Make the sentence negative: They will have been waiting for 2 hours when the train arrives."},
                {'category_id': 12, 'task_number': 3, 'content': "Ask a question: She will have been studying English for 10 years by next year."}
            ]

            for task_data in tasks_data:
                task_id = f"{task_data['category_id']:02d}{task_data['task_number']:02d}"
                try:
                    task = Task(**task_data)
                    db.session.add(task)
                    db.session.commit()
                    print(f"Задача {task_id} добавлена")
                except IntegrityError:
                    db.session.rollback()
                    print(f"Задача {task_id} уже существует")

            print("\nБаза данных успешно инициализирована!")
            print("=" * 40)
            print("Данные для входа:")
            print(f"Администратор: admin / admin123")
            print(f"Студент: student / student123")
            print("=" * 40)

        except Exception as e:
            db.session.rollback()
            print(f"Критическая ошибка: {e}")
            raise


if __name__ == '__main__':
    init_db()
