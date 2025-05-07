from app.payment import bp
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user







@bp.route('/payments')
@login_required
def payments():
    return render_template('payment/payments.html')