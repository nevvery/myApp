import string
from typing import List, Type

from app import db
from transliterate import translit
from app.models import Parent
import secrets
from sqlalchemy.orm import Session
from sqlalchemy import or_


def make_user(db_session: Session, name: str, surname: str, patronymic: str = None) -> tuple[str, str] | None:
    if not isinstance(name, str):
        raise TypeError('Name must be strings')
    if not isinstance(surname, str):
        raise TypeError('Surname must be strings')
    if not isinstance(patronymic, str):
        raise TypeError('Patronymic must be strings')

    username = generate_username(db_session=db_session, name=name, surname=surname)
    password = generate_password()

    try:
        add_user_to_db(db_session=db_session, username=username, password=password, name=name, surname=surname,
                       patronymic=patronymic)
        return username, password
    except Exception as e:
        db_session.rollback()
        raise Exception(e)


def generate_username(db_session: Session, name: str, surname: str) -> str:
    name_latin = translit(name, 'ru', reversed=True).lower()
    surname_latin = translit(surname, 'ru', reversed=True).lower()

    base_login = f'{name_latin[0]}.{surname_latin}'

    login = base_login
    suffix = 0

    while db_session.query(Parent).filter(Parent.username == login).scalar():
        login = f'{base_login}{suffix}'
        suffix += 1

    return login


def generate_password() -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(8))


def add_user_to_db(db_session: Session, username: str, password: str, name: str, surname: str,
                   patronymic: str = None) -> None:
    user = Parent(username=username, name=name, surname=surname, patronymic=patronymic)

    user.set_password(password)

    db_session.add(user)
    db_session.commit()


def get_user_select2(query: str, db_session: Session) -> list[Type[Parent]]:
    if not query:
        return db_session.query(Parent).order_by(Parent.surname).limit(10).all()

    return (
        db_session.query(Parent).filter(
            or_(
                Parent.name.ilike(f'%{query}%'),
                Parent.surname.ilike(f'%{query}%'),
                Parent.patronymic.ilike(f'%{query}%'),
            )
        ).order_by(Parent.surname).limit(10).all()
    )
