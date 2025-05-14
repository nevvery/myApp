from app.admin_panel import bp

from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_security import roles_required, login_required

from app import db
from app.models import Parent
from app.security import user_datastore
from app.admin_panel.form import AddUserForm, FindUserForm, ConfirmResetPasswordForm, ChangeRoleForm
from app.admin_panel.services import make_user, get_user_select2, generate_password, add_role_for_parent
from app.admin_panel.services import save_to_excel


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


@bp.route('/admin-panel/find_parent', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def admin_panel_find_parent():
    form = FindUserForm()

    if request.method == 'POST':
        parent_id = int(form.list_user.data)
        parent = db.session.get(Parent, parent_id)

        if not parent:
            flash('Родитель не найден', 'danger')
            return redirect(url_for('admin.admin_panel_find_parent'))

    return render_template('admin/find_parent.html', form=form)


@bp.route('/admin-panel/search-parents', methods=['GET'])
@login_required
@roles_required('admin')
def admin_panel_search_parents():
    query: str = request.args.get('q', '').strip()

    parents = get_user_select2(query=query, db_session=db.session)

    results = [
        {
            'id': parent.id,
            'text': ' '.join([name for name in [parent.name, parent.surname, parent.patronymic] if name]),
            'fs_uniquifier': parent.fs_uniquifier
        }
        for parent in parents
    ]
    return jsonify({'results': results})


@bp.route('/admin-panel/reset_password/<fs_uniquifier>', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def admin_panel_reset_password(fs_uniquifier: str):
    parent: Parent = user_datastore.find_user(fs_uniquifier=fs_uniquifier)
    form = ConfirmResetPasswordForm()

    if form.is_submitted():
        password: str = generate_password()
        parent.set_password(password)
        flash(f'Пароль успешно изменен на {password}!', 'success')
        return redirect(url_for('admin.admin_panel'))

    return render_template('admin/reset_password.html', form=form, parent=parent)


@bp.route('/admin-panel/change_role/<fs_uniquifier>', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def admin_panel_change_role(fs_uniquifier):
    form = ChangeRoleForm()

    if form.validate_on_submit():
        role_name, parent_name = add_role_for_parent(db_session=db.session, uds=user_datastore,
                                                     fs_uniquifier=fs_uniquifier, form=form)

        flash(f"Роль - {role_name} успешно добавлена пользователю {parent_name}!")
        return redirect(url_for('admin.admin_panel'))

    return render_template('admin/change_role.html', form=form)


@bp.route('/admin-panel/download_excel', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def admin_panel_download_excel():
    save_to_excel(db.session)
    return redirect(url_for('admin.admin_panel'))
