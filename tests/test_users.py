from jose import jwt
from app import schemas
from app.oauth2 import ALGORITHM, SECRET_KEY
import pytest

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

@pytest.mark.parametrize("email, password, status_code",
    [
        ('test@test.com', 'wrong_pass', 403),
        ('bad_Format', 'wrong_pass', 403),
        (None, 'wrong_pass', 422),
        ("test@test.com", None, 422),
        ('wrongemail@email.com','wrong_pass', 403),
    ])
def test_incorrent_login(client,email,password, status_code):
    res = client.post("/login", data={'username': email, 'password':password})

    assert res.status_code == status_code
    if status_code == 403:
        assert res.json()['detail'] == "Invalid Credentials"
    elif status_code == 422:
        res.json()['detail'][0]['type']='value_error.missing'

def test_read_user(client, test_user):
    id = test_user['id']
    res = client.get(f"/users/{id}/")
    print(res.json())
    user = schemas.UserResponse(**res.json())
    print(user)
    assert user.id == id
    assert res.status_code == 200

@pytest.mark.parametrize("id, status_code",
    [
        ('4', 404),
        (4, 404),
    ])
def test_get_wrong_user(client, id, status_code):
    res = client.get(f"/users/{id}/")
    print(res.json())
    assert res.json()['detail'] == f'User with id: {id} does not exist'
    assert res.status_code == status_code

#test_update
#test_update_wrong_user
#test_delete
#test_delete_wrong_user
