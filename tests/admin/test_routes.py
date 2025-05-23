import pytest
from unittest.mock import patch
from app.models import Parent


def test_admin_panel_reset_password_success(auth_client, db_session):
    parent = Parent(id=1, name='Степан', surname='Иванов', patronymic='Иванович', username='s.ivanov', fs_uniquifier='123')
    parent.set_password('<PASSWORD>')

    db_session.add(parent)
    db_session.commit()

    with patch('app.admin_panel.routes.generate_password', return_value='new_password123'):
        response = auth_client.post(
            '/admin/admin-panel/find_parent',
            data={
                'list_user': '1',
                'submit': 'Сбросить пароль'
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert 'Пароль успешно изменен на bV38Bhb0!' in response.data.decode('utf-8')

        assert parent.verify_password('<PASSWORD>') is False
        assert parent.verify_password("new_password123") is True


def test_admin_panel_find_parent_invalid_id(auth_client):
    response = auth_client.post(
        '/admin/admin-panel/find_parent',
        data={
            'list_user': '9999',
            'submit': 'Сбросить пароль'
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert 'Родитель не найден' in response.data.decode('utf-8')


def test_admin_panel_find_parent_get(auth_client):
    response = auth_client.get(
        '/admin/admin-panel/find_parent',
    )
    assert response.status_code == 200
    assert '<h1>Найти пользователя</h1>' in response.data.decode('utf-8')


def test_admin_panel_search_parents(auth_client, db_session):
    parent1 = Parent(id=1, name='Степан', surname='Иванов', patronymic='Иванович', username='s.ivanov', fs_uniquifier='123')
    parent1.set_password('<PASSWORD1>')

    parent2 = Parent(id=2, name='Руслан', surname='Щербак', patronymic=None, username='r.scherbak', fs_uniquifier='124')
    parent2.set_password('<PASSWORD2>')

    db_session.add_all([parent1, parent2])
    db_session.commit()

    response = auth_client.get('admin/admin-panel/search-parents?q=Степан')
    assert response.status_code == 200
    data = response.json
    assert len(data['results']) == 1
    assert data['results'][0] == {'fs_uniquifier': '123','id': 1, 'text': 'Степан Иванов Иванович'}

    # Пустой запрос
    response = auth_client.get('admin/admin-panel/search-parents')
    assert response.status_code == 200
    data = response.json
    assert len(data['results']) == 3


def test_admin_panel_add(auth_client, db_session):
    with patch('app.admin_panel.routes.make_user', return_value=('s.ivanov', 'password123')):
        response = auth_client.post(
            '/admin/admin-panel/add',
            data={
                'name': 'Ruslan',
                'surname': 'Ivanov',
                "patronymic": 'Ivanovich',
                'submit': 'Submit'
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert ('Пользователь c логином '
                's.ivanov и паролем password123 успешно добавлен!') in response.data.decode('utf-8')
