from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.main import bp
from app import db
from app.models import Task, TaskCategory, Solution, User
from app.main.forms import SolutionForm
from datetime import datetime


@bp.route('/')
@bp.route('/index')
def index():
    """Главная страница приложения"""
    categories = TaskCategory.query.all()
    return render_template('main/index.html', title='Home', categories=categories)


@bp.route('/category/<int:category_id>')
def category(category_id):
    """Страница категории заданий"""
    category = TaskCategory.query.get_or_404(category_id)
    tasks = Task.query.filter_by(category_id=category.id).order_by(Task.task_number).all()
    form = SolutionForm() if current_user.is_authenticated and not current_user.is_admin else None
    return render_template('main/category.html',
                           title=category.name,
                           category=category,
                           tasks=tasks,
                           form=form)


@bp.route('/dashboard')
@login_required
def dashboard():
    """Страница личного кабинета пользователя"""
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
        
    solutions = Solution.query.filter_by(user_id=current_user.id).order_by(Solution.submitted_at.desc()).all()
    form = SolutionForm()
    return render_template('main/dashboard.html',
                           title='Личный кабинет',
                           solutions=solutions,
                           form=form)


@bp.route('/submit_solution', methods=['GET', 'POST'])
@login_required
def submit_solution():
    if current_user.is_admin:
        flash('Эта страница доступна только для студентов.', 'warning')
        return redirect(url_for('admin.dashboard'))
        
    form = SolutionForm()
    if form.validate_on_submit():
        solution = Solution(
            user_id=current_user.id,
            task_id=form.task_id.data,
            content=form.content.data,
            submitted_at=datetime.utcnow()
        )
        db.session.add(solution)
        db.session.commit()
        flash('Решение успешно отправлено на проверку!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('main/submit_solution.html', form=form)
