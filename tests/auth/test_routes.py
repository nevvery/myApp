import pytest
from unittest.mock import patch
from app.models import Parent
from flask_security import current_user
import secrets


def test_login_invalid(client, db_session, app):
    with app.app_context():
        parent = Parent(name='Ruslan', surname='Ivanov', patronymic='Ivanovich', username='r.ivanov',
                        fs_uniquifier=secrets.token_urlsafe())
        parent.set_password('<PASSWORD>')

        db_session.add(parent)
        db_session.commit()

    response = client.post(
        '/auth/login',
        data={
            'username': 'r.ivanov',
            'password': '<invalid>',
            'remember_me': True,
            'submit': 'Sign In',
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert 'Неправильный логин или пароль' in response.data.decode('utf-8')

    response = client.post(
        '/auth/login',
        data={
            'username': 'invalid',
            'password': '<PASSWORD>',
            'remember_me': True,
            'submit': 'Sign In'
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert 'Неправильный логин или пароль' in response.data.decode('utf-8')


def test_login_valid(client, db_session, app):
    parent = Parent(name='Ruslan', surname='Ivanov', patronymic='Ivanovich', username='r.ivanov',
                    fs_uniquifier=secrets.token_urlsafe())
    parent.set_password('<PASSWORD>')

    db_session.add(parent)
    db_session.commit()

    with app.test_request_context():
        response = client.post(
            '/auth/login',
            data={
                'username': 'r.ivanov',
                'password': '<PASSWORD>',
                'remember_me': True,
                'submit': 'Sign In'
            },
            follow_redirects=True
        )

        assert response.status_code == 200

        assert current_user.is_authenticated
