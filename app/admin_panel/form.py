from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired


class AddUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Username', validators=[DataRequired()])
    patronymic = StringField('Patronymic', validators=[DataRequired()])
    submit = SubmitField('Submit')