def test_create_employee(client, app, authentication_headers):
    response = client.post('/api/employees/', json={
        "firstname": "John",
        "lastname": "Doe",
        "email": "test@test.com",
        "password": "password",
        "is_admin": True,
    }, headers=authentication_headers(is_admin=True))
    assert response.json["id"] == 2


def test_update_employee(client, app, authentication_headers):
    response = client.patch('/api/employees/2', json={
        "email": "test@test.test",
    }, headers=authentication_headers(is_admin=True))
    assert response.json["message"] == "Updated"


def test_get_employee(client, app, authentication_headers):
    response = client.get('/api/employees/2', headers=authentication_headers(is_admin=True))
    assert response.json['firstname'] == "John" and response.json['email'] == "test@test.test"


def test_get_employees(client, app, authentication_headers):
    response = client.get('/api/employees/', headers=authentication_headers(is_admin=True))
    assert response.json[1]['firstname'] == "John" and response.json[1]['email'] == "test@test.test"
