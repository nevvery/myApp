from app.main import bp
from flask_login import login_required
from flask import render_template, redirect, url_for


@bp.route('/')
@login_required
def index():
    return render_template('index.html')



@bp.route('/payments')
@login_required
def payments():
    return render_template('payments.html')


