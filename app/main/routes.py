from app.main import bp
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash
from app.main.form import ProfileForm
from app.main.services import tye_children_to_parent
from app import db
from app.models import Parent


@bp.route('/')
@login_required
def index():
    return render_template('index.html')


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()

    if form.validate_on_submit():
        a = tye_children_to_parent(name_children=form.name.data, surname_children=form.surname.data,
                                   patronymic_children=form.patronymic.data, group_children=form.group.data,
                                   user_parent=current_user, db_session=db.session)
        flash('Ребенок успешно добавлен!')
        return redirect(url_for('main.profile'))

    return render_template('profile.html', form=form)
