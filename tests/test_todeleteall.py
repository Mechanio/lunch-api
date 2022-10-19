import os


def test_delete_restaurant(client, app, authentication_headers):
    response = client.delete('/api/restaurants/1', headers=authentication_headers(is_admin=True))
    assert response.json['message'] == "Deleted"


def test_delete_employee(client, app, authentication_headers):
    response = client.delete('/api/employees/2', headers=authentication_headers(is_admin=True))
    assert response.json['message'] == "Deleted"


def test_delete_menu(client, app, authentication_headers):
    response = client.delete('/api/menus/1', headers=authentication_headers(is_admin=True))
    assert response.json['message'] == "Deleted"


def test_delete_database():
    os.remove("test.db")
    assert os.path.exists("test.db") is False
