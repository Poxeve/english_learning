# Формы для административной части приложения
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    TextAreaField,
    SubmitField,
    BooleanField,
    SelectField
)
from wtforms.validators import DataRequired, NumberRange, Optional, Length, ValidationError

class FeedbackForm(FlaskForm):
    """Форма для отправки отзыва о решении"""
    feedback = TextAreaField('Отзыв', validators=[
        DataRequired(),
        Length(min=10, max=500, message='Отзыв должен быть от 10 до 500 символов')
    ])
    submit = SubmitField('Отправить отзыв')

class TaskForm(FlaskForm):
    """Форма для создания и редактирования заданий"""
    category = SelectField('Категория', coerce=int, validators=[DataRequired()])
    content = TextAreaField('Содержание задания', validators=[
        DataRequired(),
        Length(min=10, max=1000, message='Содержание задания должно быть от 10 до 1000 символов')
    ])
    submit = SubmitField('Добавить задание')

    def validate_task_number(self, field):
        try:
            number = int(field.data)
            if number <= 0:
                raise ValidationError('Номер задания должен быть положительным числом')
        except ValueError:
            raise ValidationError('Номер задания должен быть числом')

class CategoryForm(FlaskForm):
    """Форма для создания и редактирования категорий заданий"""
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    is_active = BooleanField('Active', default=True, validators=[Optional()])
    submit = SubmitField('Create Category')

    class FeedbackForm(FlaskForm):
        feedback = TextAreaField('Your comment', validators=[DataRequired()])
        submit = SubmitField('Send feedback')