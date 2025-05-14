import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db
from app.models import Parent, Role
from config import TestConfig
from app.security import user_datastore


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
        fs_uniquifier='999'
    )
    user.set_password("admin123")

    role_admin = Role(name="admin", description="Administrator")
    role_parent = Role(name='parent', description="Parent Role")
    db_session.add_all([user, role_admin, role_parent])
    db_session.flush()
    user_datastore.add_role_to_user(user, role_admin)
    db_session.commit()



    with client:
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123',
            'remember_me': 'y'
        })
        yield client
