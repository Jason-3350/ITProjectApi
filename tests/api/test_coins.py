import pytest

from api.models import Coins


@pytest.mark.django_db
def test_get_coin(user, auth_client):
    coin = Coins()
    coin.id = 1
    coin.user_id = user['id']
    coin.coin = 10
    coin.save()
    coin.refresh_from_db()
    response = auth_client.get(f"/users/{user['id']}/coins")
    assert response.status_code == 200


@pytest.mark.django_db
def test_put_coin(user, auth_client):
    coin = Coins()
    coin.id = 1
    coin.user_id = user['id']
    coin.coin = 10
    coin.save()
    coin.refresh_from_db()
    put_coin = dict(newCoin=20)
    response = auth_client.put(f"/users/{user['id']}/coins", put_coin)
    assert response.status_code == 205
    coin.refresh_from_db()
    new_coin = Coins.objects.all().first()
    assert new_coin.coin == put_coin['newCoin']
