import json
import pytest
from app import create_app, db
from app.models import TaskCategory, Task

@pytest.fixture
def app():
    app = create_app('config.TestConfig')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_categories_empty(client):
    """Проверка получения категорий, когда их нет"""
    response = client.get('/api/categories')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0

def test_create_category(client):
    """Тест создания новой категории"""
    category_data = {
        'name': 'Grammar',
        'description': 'Grammar exercises'
    }
    response = client.post('/api/categories',
                          data=json.dumps(category_data),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == category_data['name']
    assert data['description'] == category_data['description']
    assert 'id' in data

def test_create_duplicate_category(client):
    """Проверьте создание категории с дублирующимся именем"""
    # Создать первую категориюy
    category_data = {
        'name': 'Grammar',
        'description': 'Grammar exercises'
    }
    client.post('/api/categories',
                data=json.dumps(category_data),
                content_type='application/json')
    
    # Попытка создать дубликат
    response = client.post('/api/categories',
                          data=json.dumps(category_data),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'message' in data
    assert 'already exists' in data['message']

def test_get_category(client):
    """Тест на получение определенной категории"""
    category_data = {
        'name': 'Grammar',
        'description': 'Grammar exercises'
    }
    create_response = client.post('/api/categories',
                                data=json.dumps(category_data),
                                content_type='application/json')
    category_id = json.loads(create_response.data)['id']
    
    # Получить категорию
    response = client.get(f'/api/categories/{category_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == category_data['name']
    assert data['description'] == category_data['description']

def test_update_category(client):
    """Тестовое обновление категории"""
    category_data = {
        'name': 'Grammar',
        'description': 'Grammar exercises'
    }
    create_response = client.post('/api/categories',
                                data=json.dumps(category_data),
                                content_type='application/json')
    category_id = json.loads(create_response.data)['id']

    update_data = {
        'name': 'Advanced Grammar',
        'description': 'Advanced grammar exercises'
    }
    response = client.put(f'/api/categories/{category_id}',
                         data=json.dumps(update_data),
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == update_data['name']
    assert data['description'] == update_data['description']

def test_delete_category(client):
    """Тест удаления категории"""
    category_data = {
        'name': 'Grammar',
        'description': 'Grammar exercises'
    }
    create_response = client.post('/api/categories',
                                data=json.dumps(category_data),
                                content_type='application/json')
    category_id = json.loads(create_response.data)['id']
    
    # Удалить категорию
    response = client.delete(f'/api/categories/{category_id}')
    assert response.status_code == 204
    
    # Проверка, что удалено
    get_response = client.get(f'/api/categories/{category_id}')
    assert get_response.status_code == 404

def test_get_tasks_empty(client):
    """Проверrf получение задач, когда их нет"""
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0

def test_create_task(client):
    """Тест создания новой задачи"""
    # Create a category first
    category_data = {
        'name': 'Grammar',
        'description': 'Grammar exercises'
    }
    create_category_response = client.post('/api/categories',
                                         data=json.dumps(category_data),
                                         content_type='application/json')
    category_id = json.loads(create_category_response.data)['id']

    task_data = {
        'category_id': category_id,
        'task_number': 1,
        'content': 'Complete the sentence'
    }
    response = client.post('/api/tasks',
                          data=json.dumps(task_data),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['category_id'] == task_data['category_id']
    assert data['task_number'] == task_data['task_number']
    assert data['content'] == task_data['content']
    assert 'id' in data
    assert 'full_id' in data

def test_create_task_invalid_category(client):
    """Тест создания задачи с недопустимой категорией"""
    task_data = {
        'category_id': 999,
        'task_number': 1,
        'content': 'Complete the sentence'
    }
    response = client.post('/api/tasks',
                          data=json.dumps(task_data),
                          content_type='application/json')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'message' in data
    assert 'not found' in data['message']

def test_create_duplicate_task(client):
    """Тест создания задачи с повторяющимся номером в категории"""
    category_data = {
        'name': 'Grammar',
        'description': 'Grammar exercises'
    }
    create_category_response = client.post('/api/categories',
                                         data=json.dumps(category_data),
                                         content_type='application/json')
    category_id = json.loads(create_category_response.data)['id']

    task_data = {
        'category_id': category_id,
        'task_number': 1,
        'content': 'Complete the sentence'
    }
    client.post('/api/tasks',
                data=json.dumps(task_data),
                content_type='application/json')

    response = client.post('/api/tasks',
                          data=json.dumps(task_data),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'message' in data
    assert 'already exists' in data['message']

def test_get_task(client):
    """Тест на получение конкретного задания"""
    category_data = {
        'name': 'Grammar',
        'description': 'Grammar exercises'
    }
    create_category_response = client.post('/api/categories',
                                         data=json.dumps(category_data),
                                         content_type='application/json')
    category_id = json.loads(create_category_response.data)['id']
    
    task_data = {
        'category_id': category_id,
        'task_number': 1,
        'content': 'Complete the sentence'
    }
    create_task_response = client.post('/api/tasks',
                                     data=json.dumps(task_data),
                                     content_type='application/json')
    task_id = json.loads(create_task_response.data)['id']

    response = client.get(f'/api/tasks/{task_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['category_id'] == task_data['category_id']
    assert data['task_number'] == task_data['task_number']
    assert data['content'] == task_data['content']

def test_update_task(client):
    """Тестовое обновление задачи"""
    category_data = {
        'name': 'Grammar',
        'description': 'Grammar exercises'
    }
    create_category_response = client.post('/api/categories',
                                         data=json.dumps(category_data),
                                         content_type='application/json')
    category_id = json.loads(create_category_response.data)['id']
    
    task_data = {
        'category_id': category_id,
        'task_number': 1,
        'content': 'Complete the sentence'
    }
    create_task_response = client.post('/api/tasks',
                                     data=json.dumps(task_data),
                                     content_type='application/json')
    task_id = json.loads(create_task_response.data)['id']

    update_data = {
        'category_id': category_id,
        'task_number': 2,
        'content': 'Updated task content'
    }
    response = client.put(f'/api/tasks/{task_id}',
                         data=json.dumps(update_data),
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['task_number'] == update_data['task_number']
    assert data['content'] == update_data['content']

def test_delete_task(client):
    """Тест удаления задачи"""
    category_data = {
        'name': 'Grammar',
        'description': 'Grammar exercises'
    }
    create_category_response = client.post('/api/categories',
                                         data=json.dumps(category_data),
                                         content_type='application/json')
    category_id = json.loads(create_category_response.data)['id']
    
    task_data = {
        'category_id': category_id,
        'task_number': 1,
        'content': 'Complete the sentence'
    }
    create_task_response = client.post('/api/tasks',
                                     data=json.dumps(task_data),
                                     content_type='application/json')
    task_id = json.loads(create_task_response.data)['id']

    response = client.delete(f'/api/tasks/{task_id}')
    assert response.status_code == 204

    get_response = client.get(f'/api/tasks/{task_id}')
    assert get_response.status_code == 404 