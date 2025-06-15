from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.admin import bp
from app.admin.forms import TaskForm, FeedbackForm
from app.models import Task, TaskCategory, Solution


@bp.before_request
@login_required
def before_request():
    """Проверка прав администратора перед каждым запросом"""
    if not current_user.is_admin:
        flash('У вас нет доступа к этой странице.', 'danger')
        return redirect(url_for('main.index'))


@bp.route('/')
def index():
    """Перенаправление на страницу решений"""
    return redirect(url_for('admin.solutions'))


@bp.route('/solutions')
def solutions():
    """Список решений с пагинацией"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Фильтр для непроверенных решений + пагинация
    solutions_pagination = db.session.query(Solution, User.username) \
        .join(User, Solution.user_id == User.id) \
        .filter(Solution.is_reviewed == False) \
        .order_by(Solution.submitted_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('admin/solutions.html',
                           title='Решения для проверки',
                           solutions=solutions_pagination)


@bp.route('/solution/<int:solution_id>', methods=['GET', 'POST'])
def solution(solution_id):
    """Просмотр и оценка конкретного решения"""
    solution = Solution.query.get_or_404(solution_id)
    form = FeedbackForm()

    if form.validate_on_submit():
        try:
            solution.feedback = form.feedback.data
            solution.is_reviewed = True
            solution.reviewed_at = datetime.utcnow()
            solution.reviewed_by = current_user.id
            db.session.commit()
            flash('Отзыв успешно добавлен!', 'success')
            return redirect(url_for('admin.solutions'))
        except Exception as e:
            db.session.rollback()
            flash('Произошла ошибка при сохранении отзыва.', 'danger')

    elif request.method == 'GET':
        form.feedback.data = solution.feedback

    # Получаем связанные данные
    task = Task.query.get(solution.task_id)
    student = User.query.get(solution.user_id)

    return render_template('admin/solution.html',
                           title=f'Проверка решения #{solution.id}',
                           solution=solution,
                           task=task,
                           student=student,
                           form=form)


@bp.route('/users')
def users():
    """Список всех пользователей"""
    users = User.query.order_by(User.username.asc()).all()
    return render_template('admin/users.html',
                           title='User Management',
                           users=users)


@bp.route('/tasks')
def tasks():
    """Список всех заданий с группировкой по категориям"""
    tasks = Task.query.order_by(Task.category_id.asc(), Task.task_number.asc()).all()
    return render_template('admin/tasks.html',
                           title='Task Management',
                           tasks=tasks)


@bp.route('/dashboard')
@login_required
def dashboard():
    """Страница панели управления администратора"""
    if not current_user.is_admin:
        flash('У вас нет доступа к этой странице.', 'danger')
        return redirect(url_for('main.index'))
    
    tasks = Task.query.order_by(Task.category_id.asc(), Task.task_number.asc()).all()
    categories = TaskCategory.query.all()
    solutions = Solution.query.order_by(Solution.submitted_at.desc()).all()
    
    form = TaskForm()
    form.category.choices = [(c.id, c.name) for c in categories]
    
    feedback_form = FeedbackForm()
    
    return render_template('admin/dashboard.html',
                           title='Панель преподавателя',
                           tasks=tasks,
                           solutions=solutions,
                           form=form,
                           feedback_form=feedback_form)


@bp.route('/add_task', methods=['POST'])
@login_required
def add_task():
    if not current_user.is_admin:
        flash('У вас нет доступа к этой странице.', 'danger')
        return redirect(url_for('main.index'))
    
    form = TaskForm()
    form.category.choices = [(c.id, c.name) for c in TaskCategory.query.all()]
    
    if form.validate_on_submit():
        try:
            # Находим последний номер задания в выбранной категории
            last_task = Task.query.filter_by(category_id=form.category.data).order_by(Task.task_number.desc()).first()
            next_task_number = 1 if last_task is None else last_task.task_number + 1
            
            task = Task(
                category_id=form.category.data,
                task_number=next_task_number,
                content=form.content.data,
                created_at=datetime.utcnow()
            )
            db.session.add(task)
            db.session.commit()
            flash('Задание успешно добавлено!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Произошла ошибка при добавлении задания: {str(e)}', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'danger')
    
    return redirect(url_for('admin.dashboard'))


@bp.route('/review_solution/<int:solution_id>', methods=['POST'])
@login_required
def review_solution(solution_id):
    """Страница проверки решения"""
    if not current_user.is_admin:
        flash('У вас нет доступа к этой странице.', 'danger')
        return redirect(url_for('main.index'))
    
    solution = Solution.query.get_or_404(solution_id)
    form = FeedbackForm()
    
    if form.validate_on_submit():
        solution.feedback = form.feedback.data
        solution.is_reviewed = True
        solution.reviewed_at = datetime.utcnow()
        solution.reviewed_by = current_user.id
        db.session.commit()
        flash('Отзыв успешно добавлен!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'danger')
    return redirect(url_for('admin.dashboard'))