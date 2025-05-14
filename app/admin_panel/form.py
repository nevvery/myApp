from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import Parent, Role
from app import db


class AddUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Username', validators=[DataRequired()])
    patronymic = StringField('Patronymic')
    submit = SubmitField('Submit')


class FindUserForm(FlaskForm):
    list_user = StringField('ФИО родителя', validators=[DataRequired()],
                            render_kw={'class': 'select2', 'data-placeholder': 'Введите ФИО родителя'})

    def validate_list_user(self, field):
        try:
            parent_id = int(field.data)
        except ValueError:
            raise ValidationError('Неверный формат ID родителя.')
        if not db.session.get(Parent, parent_id):
            raise ValidationError('Выбранный родитель не существует.')


class ConfirmResetPasswordForm(FlaskForm):
    submit = SubmitField('Да')


class ChangeRoleForm(FlaskForm):
    submit = SubmitField('Отправить')
    role = SelectField('Выберите роль', validators=[DataRequired()], coerce=int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in db.session.query(Role).all() if role.name != 'admin']
