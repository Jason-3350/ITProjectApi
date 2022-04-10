import pytest
from rest_framework.test import APIClient


# client = APIClient()


@pytest.fixture
def user(client):
    regUser = dict(
        id=1,
        username="ying",
        userEmail="ying@gmail.com",
        password="ying123456",
    )
    client.post("/register", regUser)
    return regUser


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_client(user, client):
    loginPayload = dict(
        username=user['userEmail'],
        password=user['password'],
    )
    response = client.post('/token', loginPayload)
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    return client


