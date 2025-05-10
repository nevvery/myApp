from sqlalchemy.sql.coercions import expect

from config import BASE_DIR
from app.payment.form import PaymentForm
from app.models import Child, Payment

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from datetime import date, datetime, time

from flask import current_app
import os
import uuid

from unidecode import unidecode


def add_payment_to_db(db_session, pdf_file: FileStorage, value: str, id_child: str, date_pay: date) -> None:
    child = db_session.query(Child).filter_by(id=int(id_child)).first()

    if not child:
        raise ValueError(f'Child with id {id_child} not found')

    path_pdf_file = save_pdf_file(pdf_file=pdf_file, name_child=child.name, surname_child=child.surname,
                                  date_pay=date_pay, value=value)

    date_pay_with_time = datetime.combine(date_pay, time(0, 0))

    try:
        payment = Payment(value=float(value), date_pay=date_pay_with_time, path_pdf_file=path_pdf_file,
                          id_child=id_child)
        db_session.add(payment)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise Exception(e)


def save_pdf_file(pdf_file: FileStorage, name_child: str, surname_child: str, date_pay: date, value: str) -> str:
    # Руслан_Иванов_2025-09-05_15000.pdf

    if not isinstance(pdf_file, FileStorage):
        raise ValueError('pdf_file must be of type FileStorage')

    name_child = unidecode(name_child)
    surname_child = unidecode(surname_child)

    unique_id = uuid.uuid4().hex[:8]

    filename = f'{name_child}_{surname_child}_{date_pay}_{value}_{unique_id}.pdf'
    filename = secure_filename(filename)

    pdf_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    try:
        pdf_file.save(pdf_file_path)
    except OSError as e:
        raise OSError(f'Error saving file: {str(e)}')

    return pdf_file_path
