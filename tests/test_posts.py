from app import schemas
import pytest



# def test_create_post(authorized_client):
#     res = authorized_client.post("/posts/", json={'title': 'title1',
#                                        'content': 'content1'})
#     new_user = schemas.UserResponse(**res.json())
#     assert res.status_code == 201
#     assert new_user.email == 'g@g.com'

def test_get_all_posts(authorized_client):
    res = authorized_client.get("/posts/")
    assert res.status_code == 204
    assert res.json()['detail'] == 'No posts found'