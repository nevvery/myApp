from app.auth import bp
from flask import render_template, url_for, redirect, flash
from app.auth.form import LoginForm
from app import db
from app.models import Parent, Role
from flask_security import login_user, Security, SQLAlchemyUserDatastore, logout_user

user_datastore = SQLAlchemyUserDatastore(db, Parent, Role)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = user_datastore.find_user(username=form.username.data)

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
