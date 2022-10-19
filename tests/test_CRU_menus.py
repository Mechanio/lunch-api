def test_create_menu(client, app, authentication_headers):
    response = client.post('/api/menus/', json={
        "restaurant_id": 1,
        "monday": "Soup",
        "tuesday": "Potato",
        "wednesday": "Cheese",
        "thursday": "Salad",
        "friday": "Tomato",
        "saturday": "Bread",
        "sunday": "Cookies"
    }, headers=authentication_headers(is_admin=True))
    assert response.json["id"] == 1


def test_update_menu(client, app, authentication_headers):
    response = client.patch('/api/menus/1', json={
        "tuesday": "Bacon",
    }, headers=authentication_headers(is_admin=True))
    assert response.json["message"] == "Updated"


def test_get_menu(client, app):
    response = client.get('/api/menus/1')
    assert response.json['tuesday'] == "Bacon" and response.json['friday'] == "Tomato"


def test_get_menus(client, app):
    response = client.get('/api/menus/')
    assert response.json[0]['tuesday'] == "Bacon" and response.json[0]['friday'] == "Tomato"
