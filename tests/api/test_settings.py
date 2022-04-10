import pytest


@pytest.mark.django_db
def test_get_coin_205(user, auth_client):
    payload = dict(
        username="ying",
        oldPassword="ying123456",
        newPassword="ying456789",
    )
    response = auth_client.post('/settings', payload)
    assert response.status_code == 205


@pytest.mark.django_db
def test_get_coin_203(user, auth_client):
    payload = dict(
        username="ying",
        oldPassword="ying",
        newPassword="ying456789",
    )
    response = auth_client.post('/settings', payload)
    assert response.status_code == 203
