import pytest
from app.admin_panel.services import get_user_select2, add_user_to_db, generate_username
from app.models import Parent


def test_get_user_select2_empty_query(db_session):
    parent1 = Parent(id=1, name='Степан', surname='Иванов', patronymic='Иванович', username='s.ivanov', fs_uniquifier='124')
    parent1.set_password('<PASSWORD1>')

    parent2 = Parent(id=2, name='Руслан', surname='Щербак', patronymic=None, username='r.scherbak', fs_uniquifier='123')
    parent2.set_password('<PASSWORD2>')

    db_session.add_all([parent1, parent2])
    db_session.commit()

    parents = get_user_select2(query='', db_session=db_session)

    assert len(parents) == 2
    assert parents[0].name == "Степан"
    assert parents[1].name == 'Руслан'


def test_get_user_select2_search_by_name(db_session):
    parent = Parent(id=1, name='Степан', surname='Иванов', patronymic='Иванович', username='s.ivanov', fs_uniquifier='123')
    parent.set_password('<PASSWORD>')

    db_session.add(parent)
    db_session.commit()

    parents = get_user_select2(query='Степан', db_session=db_session)

    assert len(parents) == 1
    assert parents[0].name == 'Степан'


def test_get_user_select2_no_results(db_session):
    parents = get_user_select2(query='Неизвестно', db_session=db_session)
    assert len(parents) == 0


def test_generate_username(db_session):
    name = 'Руслан'
    surname = 'Иванов'

    result = generate_username(db_session=db_session, name=name, surname=surname)

    assert result == 'r.ivanov'


def test_user_to_db(db_session):
    name = 'Руслан'
    surname = 'Иванов'
    patronymic = "Иванович"
    username = 'r.ivanov'
    fs_uniquifier = '123'

    add_user_to_db(db_session=db_session, name=name, surname=surname, password='<PASSWORD>', username=username,
                   patronymic=patronymic, fs_uniquifier=fs_uniquifier)

    parent = db_session.query(Parent).filter(Parent.name == name).first()

    assert (parent.name, parent.surname, parent.patronymic, parent.username) == (name, surname, patronymic, username)
