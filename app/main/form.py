from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    name = StringField('Имя ребенка', validators=[DataRequired()])
    surname = StringField('Фамилия ребенка', validators=[DataRequired()])
    patronymic = StringField('Отчество ребенка', validators=[DataRequired()])
    group = StringField('Группа ребенка', validators=[DataRequired()])

    submit = SubmitField('Отправить!')
