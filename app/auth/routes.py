from app.auth import bp
from flask import render_template, url_for, redirect, flash
from app.auth.form import LoginForm
from app import db
from app.models import Parent
from flask_login import current_user, login_user, logout_user


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Parent.query.filter_by(username=form.username.data).first()

        if user is None or not user.verify_password(form.password.data):
            flash('Неправильный логин или пароль')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
