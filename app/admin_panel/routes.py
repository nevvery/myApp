from app.admin_panel import bp
from flask_login import login_required
from flask import render_template, redirect, url_for, flash
from app.admin_panel.form import AddUserForm
from app.admin_panel.services import make_user
from app import db


@bp.route('/admin-panel')
@login_required
def admin_panel():
    return render_template('admin/admin-panel.html')


@bp.route('/admin-panel/add', methods=['GET', 'POST'])
@login_required
def admin_panel_add():
    form = AddUserForm()

    if form.validate_on_submit():
        user = make_user(db_session=db.session,
                         name=form.name.data,
                         surname=form.surname.data,
                         patronymic=form.patronymic.data
                         )
        if user:
            flash(user)
            return redirect(url_for('admin.admin_panel_add'))

        flash('Пользователь успешно добавлен!')
        return redirect(url_for('admin.admin_panel'))

    return render_template('admin/add_user.html', form=form)
