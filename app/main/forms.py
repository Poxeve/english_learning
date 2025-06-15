# Формы для основного модуля приложения
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange


class SolutionForm(FlaskForm):
    """Форма для отправки решения задания"""
    task_id = IntegerField('Номер задания', validators=[
        DataRequired(),
        NumberRange(min=1, message='Номер задания должен быть положительным числом')
    ])
    content = TextAreaField('Ваше решение', validators=[
        DataRequired(),
        Length(min=1, max=1000, message='Решение должно быть от 1 до 1000 символов')
    ])
    submit = SubmitField('Отправить решение')


class FeedbackForm(FlaskForm):
    feedback = TextAreaField('Your comment', validators=[DataRequired()])
    submit = SubmitField('Send feedback')
