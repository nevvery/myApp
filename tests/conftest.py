import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db
from app.models import Parent
from config import TestConfig


@pytest.fixture
def app():
    app = create_app(config=TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session(app):
    with app.app_context():
        session = db.session
        yield session
        session.rollback()
        session.close()


@pytest.fixture
def auth_client(client, db_session):
    user = Parent(
        id=999,
        name="Admin",
        surname="Adminov",
        patronymic="Adminovich",
        username="admin",
    )
    user.set_password("admin123")
    db_session.add(user)
    db_session.commit()

    with client:
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123',
            'remember_me': 'y'
        })
        yield client
