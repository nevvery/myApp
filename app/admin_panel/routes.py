from app.admin_panel import bp
from flask_security import roles_required, login_required
from flask import render_template, redirect, url_for, flash, request, jsonify
from app.admin_panel.form import AddUserForm, ResetPasswordForm
from app.admin_panel.services import make_user, get_user_select2, generate_password
from app import db
from app.models import Parent
from flask import current_app


@bp.route('/admin-panel')
@login_required
@roles_required('admin')
def admin_panel():
    return render_template('admin/admin-panel.html')


@bp.route('/admin-panel/add', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def admin_panel_add():
    form = AddUserForm()

    if form.validate_on_submit():
        username, password = make_user(db_session=db.session,
                                       name=form.name.data,
                                       surname=form.surname.data,
                                       patronymic=form.patronymic.data
                                       )

        flash(f'Пользователь c логином {username} и паролем {password} успешно добавлен!', 'success')
        return redirect(url_for('admin.admin_panel'))

    return render_template('admin/add_user.html', form=form)


@bp.route('/admin-panel/reset_password', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def admin_panel_reset_password():
    form = ResetPasswordForm()

    print(form.list_user.data, form.submit.data)
    if form.validate_on_submit():
        parent_id = int(form.list_user.data)
        parent = db.session.get(Parent, parent_id)

        if not parent:
            flash('Родитель не найден', 'danger')
            return redirect(url_for('admin.admin_panel_reset_password'))

        new_password = generate_password()
        parent.set_password(new_password)
        db.session.commit()

        flash(f'Новый пароль для {parent.name} {parent.surname}: {new_password}', 'success')
        return redirect(url_for('admin.admin_panel'))

    return render_template('admin/reset_password.html', form=form)


@bp.route('/admin-panel/search-parents', methods=['GET'])
@login_required
@roles_required('admin')
def admin_panel_search_parents():
    query: str = request.args.get('q', '').strip()

    parents = get_user_select2(query=query, db_session=db.session)

    results = [
        {
            'id': parent.id,
            'text': ' '.join([name for name in [parent.name, parent.surname, parent.patronymic] if name])
        }
        for parent in parents
    ]
    return jsonify({'results': results})
