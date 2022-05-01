from jose import JWTError, jwt
from app import schemas
from app.oauth2 import ALGORITHM, SECRET_KEY
from .create_test_db import client, session
import pytest


@pytest.fixture()
def test_user(client):
    user_data = {'email': "test@test.com", 'password':'123'}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user 

def test_root(client,session):
    res = client.get("/")
    assert res.json().get('message') == "Hello World"
    assert res.status_code == 200


def test_create_user(client,session):
    res = client.post("/users/", json={'email': 'g@g.com',
                                       'password': '123'})
    new_user = schemas.UserResponse(**res.json())
    assert res.status_code == 201
    assert new_user.email == 'g@g.com'


def test_login_user(client,test_user):
    res = client.post("/login", data={'username': test_user['email'], 'password':test_user['password']})
    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, SECRET_KEY.get_secret_value(), algorithms=[ALGORITHM])
    assert res.status_code == 200
    assert test_user['id'] == payload['user_id']
    assert login_res.token_type == 'bearer'