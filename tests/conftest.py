import os

import pytest


@pytest.fixture
def app(monkeypatch):
    db_path = os.path.abspath("test.db")
    monkeypatch.setenv('SQLALCHEMY_DATABASE_URI', f"sqlite:///{db_path}")
    from app.main import create_app
    app = create_app()
    return app


@pytest.fixture
def client(app):
    app.testing = True
    return app.test_client()


@pytest.fixture
def authentication_headers(client):
    def _authentication_headers(is_admin: bool, refresh=False):
        if is_admin:
            email = "admintest"
            password = "admintest"
        else:
            email = "usertest"
            password = "usertest"
        response = client.post('/api/auth/login',
                               json={
                                   "email": email,
                                   "password": password,
                               })

        if response.json['message'] == f"User with email {email} doesn't exist":
            response = client.post('/api/auth/registration',
                                   json={
                                       "firstname": email,
                                       "lastname": email,
                                       "email": email,
                                       "password": password,
                                       "is_admin": is_admin,
                                   })
        if refresh:
            auth_token = response.json['refresh_token']
            headers = {"Authorization": f"Bearer {auth_token}"}
        else:
            auth_token = response.json['access_token']
            headers = {"Authorization": f"Bearer {auth_token}"}

        return headers

    return _authentication_headers
