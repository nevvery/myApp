from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    patronymic = StringField('Patronym', validators=[DataRequired()])
    group = StringField('Group', validators=[DataRequired()])

    submit = SubmitField('Submit')
