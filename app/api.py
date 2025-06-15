from flask_restful import Resource, Api, reqparse
from app.models import TaskCategory, Task
from app import db

# Initialize API
api = Api()

# Parser for task creation/updates
task_parser = reqparse.RequestParser()
task_parser.add_argument('category_id', type=int, required=True, help='Category ID is required')
task_parser.add_argument('task_number', type=int, required=True, help='Task number is required')
task_parser.add_argument('content', type=str, required=True, help='Task content is required')

# Parser for category creation/updates
category_parser = reqparse.RequestParser()
category_parser.add_argument('name', type=str, required=True, help='Category name is required')
category_parser.add_argument('description', type=str, required=False)

class CategoryResource(Resource):
    def get(self, category_id=None):
        if category_id is None:
            # Get all categories
            categories = TaskCategory.query.all()
            return [{
                'id': cat.id,
                'name': cat.name,
                'description': cat.description
            } for cat in categories]
        
        # Get specific category
        category = db.session.get(TaskCategory, category_id)
        if category is None:
            return {'message': 'Category not found'}, 404
        return {
            'id': category.id,
            'name': category.name,
            'description': category.description
        }

    def post(self):
        args = category_parser.parse_args()
        
        # Check if category with this name already exists
        if TaskCategory.query.filter_by(name=args['name']).first():
            return {'message': 'Category with this name already exists'}, 400
        
        category = TaskCategory(
            name=args['name'],
            description=args.get('description')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return {
            'id': category.id,
            'name': category.name,
            'description': category.description
        }, 201

    def put(self, category_id):
        category = db.session.get(TaskCategory, category_id)
        if category is None:
            return {'message': 'Category not found'}, 404
            
        args = category_parser.parse_args()
        
        # Check if new name conflicts with existing category
        existing = TaskCategory.query.filter_by(name=args['name']).first()
        if existing and existing.id != category_id:
            return {'message': 'Category with this name already exists'}, 400
        
        category.name = args['name']
        category.description = args.get('description')
        
        db.session.commit()
        
        return {
            'id': category.id,
            'name': category.name,
            'description': category.description
        }

    def delete(self, category_id):
        category = db.session.get(TaskCategory, category_id)
        if category is None:
            return {'message': 'Category not found'}, 404
            
        db.session.delete(category)
        db.session.commit()
        return '', 204

class TaskResource(Resource):
    def get(self, task_id=None):
        if task_id is None:
            # Get all tasks
            tasks = Task.query.all()
            return [{
                'id': task.id,
                'category_id': task.category_id,
                'task_number': task.task_number,
                'content': task.content,
                'created_at': task.created_at.isoformat(),
                'full_id': task.get_full_id()
            } for task in tasks]
        
        # Get specific task
        task = db.session.get(Task, task_id)
        if task is None:
            return {'message': 'Task not found'}, 404
            
        return {
            'id': task.id,
            'category_id': task.category_id,
            'task_number': task.task_number,
            'content': task.content,
            'created_at': task.created_at.isoformat(),
            'full_id': task.get_full_id()
        }

    def post(self):
        args = task_parser.parse_args()
        
        # Check if category exists
        category = db.session.get(TaskCategory, args['category_id'])
        if category is None:
            return {'message': 'Category not found'}, 404
        
        # Check if task with this number in category already exists
        if Task.query.filter_by(
            category_id=args['category_id'],
            task_number=args['task_number']
        ).first():
            return {'message': 'Task with this number already exists in this category'}, 400
        
        task = Task(
            category_id=args['category_id'],
            task_number=args['task_number'],
            content=args['content']
        )
        
        db.session.add(task)
        db.session.commit()
        
        return {
            'id': task.id,
            'category_id': task.category_id,
            'task_number': task.task_number,
            'content': task.content,
            'created_at': task.created_at.isoformat(),
            'full_id': task.get_full_id()
        }, 201

    def put(self, task_id):
        task = db.session.get(Task, task_id)
        if task is None:
            return {'message': 'Task not found'}, 404
            
        args = task_parser.parse_args()
        
        # Check if category exists
        category = db.session.get(TaskCategory, args['category_id'])
        if category is None:
            return {'message': 'Category not found'}, 404
        
        # Check if new task number conflicts with existing task in category
        existing = Task.query.filter_by(
            category_id=args['category_id'],
            task_number=args['task_number']
        ).first()
        if existing and existing.id != task_id:
            return {'message': 'Task with this number already exists in this category'}, 400
        
        task.category_id = args['category_id']
        task.task_number = args['task_number']
        task.content = args['content']
        
        db.session.commit()
        
        return {
            'id': task.id,
            'category_id': task.category_id,
            'task_number': task.task_number,
            'content': task.content,
            'created_at': task.created_at.isoformat(),
            'full_id': task.get_full_id()
        }

    def delete(self, task_id):
        task = db.session.get(Task, task_id)
        if task is None:
            return {'message': 'Task not found'}, 404
            
        db.session.delete(task)
        db.session.commit()
        return '', 204

# Register resources
api.add_resource(CategoryResource, '/api/categories', '/api/categories/<int:category_id>')
api.add_resource(TaskResource, '/api/tasks', '/api/tasks/<int:task_id>') 