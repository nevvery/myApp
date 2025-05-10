from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import Parent
from app import db


class AddUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Username', validators=[DataRequired()])
    patronymic = StringField('Patronymic', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ResetPasswordForm(FlaskForm):
    list_user = StringField('ФИО родителя', validators=[DataRequired()],
                            render_kw={'class': 'select2', 'data-placeholder': 'Введите ФИО родителя'})
    submit = SubmitField('Сбросить пароль')

    def validate_list_user(self, field):
        try:
            parent_id = int(field.data)
        except ValueError:
            raise ValidationError('Неверный формат ID родителя.')
        if not db.session.get(Parent, parent_id):
            raise ValidationError('Выбранный родитель не существует.')
