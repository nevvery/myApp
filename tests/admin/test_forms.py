import pytest
from app.admin_panel.form import FindUserForm
from app.models import Parent


def test_reset_password_form_valid(db_session):
    parent = Parent(id=1, name='Степан', surname='Иванов', patronymic='Иванович', username='s.ivanov',
                    fs_uniquifier='123')
    parent.set_password('<PASSWORD>')
    db_session.add(parent)
    db_session.commit()

    form = FindUserForm(list_user='1')
    assert form.validate() is True


def test_reset_password_form_invalid(db_session):
    form = FindUserForm(list_user='invalid')

    assert form.validate() is False
    assert 'Неверный формат ID родителя.' in form.list_user.errors


def test_reset_password_form_nonexistent_parent(db_session):
    form = FindUserForm(list_user='999')
    assert form.validate() is False
    assert 'Выбранный родитель не существует.' in form.list_user.errors


def test_reset_password_form_empty(db_session):
    form = FindUserForm(list_user='')
    assert form.validate() is False
    assert 'This field is required.' in form.list_user.errors
