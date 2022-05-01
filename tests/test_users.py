from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from .create_test_db import get_test_db

client = TestClient(app)

app.dependency_overrides[get_db] = get_test_db


def test_root():
    res = client.get("/")
    assert res.json().get('message') == "Hello World"
    assert res.status_code == 200
    print('asd')


def test_create_user():
    res = client.post("/users/", json={'email': 'g@g.com',
                                       'password': '123'})
    assert res.status_code == 201
    assert res.json().get('email') == 'g@g.com'


