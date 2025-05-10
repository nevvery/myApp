from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, SelectField, DateField, SubmitField, FileField
from wtforms.validators import DataRequired


class PaymentForm(FlaskForm):
    name_child = SelectField('Выберите ребенка', coerce=int, validators=[DataRequired()])
    value_pay = StringField('Укажите сумму', validators=[DataRequired()])
    date_pay = DateField('Укажите дату платежа', validators=[DataRequired()])
    pdf_file = FileField('Прикрепите PDF файл', validators=[FileRequired(), FileAllowed(['pdf'], 'Только PDF файлы!')])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.name_child.choices = [(child.id, f'{child.name} {child.surname} {child.patronymic}') for child in
                                   current_user.children]
