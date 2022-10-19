def test_create_restaurant(client, app, authentication_headers):
    response = client.post('/api/restaurants/', json={
        "name": "McDonalds",
    }, headers=authentication_headers(is_admin=True))
    assert response.json["id"] == 1


def test_update_restaurant(client, app, authentication_headers):
    response = client.patch('/api/restaurants/1', json={
        "name": "McDonald's",
    }, headers=authentication_headers(is_admin=True))
    assert response.json["message"] == "Updated"


def test_get_restaurant(client, app):
    response = client.get('/api/restaurants/1')
    assert response.json['name'] == "McDonald's"


def test_get_restaurants(client, app):
    response = client.get('/api/restaurants/')
    assert response.json[0]['name'] == "McDonald's"