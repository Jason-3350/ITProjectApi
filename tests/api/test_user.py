import pytest


# from rest_framework.test import APIClient
#
# client = APIClient()


@pytest.mark.django_db
def test_register_user(client):
    payload = dict(
        username="ying",
        userEmail="ying@gmail.com",
        password="ying123456",
    )

    response = client.post("/register", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_get_oneUser(user, auth_client):
    # loginPayload = dict(
    #     username="ying@gmail.com",
    #     password="ying123456",
    # )
    # client.post('/token', loginPayload)
    # response = client.get('/userinfo/1')
    response = auth_client.get('/userinfo/1')
    assert response.status_code == 200

    data = response.data
    assert data['username'] == user['username']
    assert data['email'] == user['userEmail']
