from werkzeug.utils import secure_filename

from app.payment import bp
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.payment.forms import PaymentForm
from app import db

from app.payment.services import add_payment_to_db


@bp.route('/payments', methods=['GET', 'POST'])
@login_required
def payments():
    form = PaymentForm()

    if form.validate_on_submit():
        add_payment_to_db(db_session=db.session,
                          pdf_file=form.pdf_file.data,
                          value=form.value_pay.data,
                          id_child=form.name_child.data,
                          date_pay=form.date_pay.data)
        flash('Платеж успешно внесен!')
        return redirect(url_for('payment.payments'))

    return render_template('payment/payments.html', form=form)
