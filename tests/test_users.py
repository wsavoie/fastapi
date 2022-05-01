from .create_test_db import client, session

def test_root(client,session):
    res = client.get("/")
    assert res.json().get('message') == "Hello World"
    assert res.status_code == 200


def test_create_user(client,session):
    res = client.post("/users/", json={'email': 'g@g.com',
                                       'password': '123'})
    assert res.status_code == 201
    assert res.json().get('email') == 'g@g.com'


