import pytest


# from rest_framework.test import APIClient

# client = APIClient()


@pytest.mark.django_db
def test_login_user(user, client):
    # regPayload = dict(
    #     username="ying",
    #     userEmail="ying@gmail.com",
    #     password="ying123456",
    # )
    # client.post("/register", regPayload)
    loginPayload = dict(
        username="ying@gmail.com",
        password="ying123456",
    )
    response = client.post('/token', loginPayload)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_user_fail(client):
    loginPayload = dict(
        username="ying@gmail.com",
        password="ying",
    )
    response = client.post('/token', loginPayload)

    assert response.status_code == 401
