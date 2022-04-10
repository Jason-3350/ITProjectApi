import pytest

from api.models import Order


@pytest.mark.django_db
def test_get_user_order(user, auth_client):
    order = Order()
    order.id = 1
    order.coin = 10
    order.rewards = 'Starbucks'
    order.qr = '1/jason/jason@gmail.com/2022-01-01/18:00:00'
    order.user_id = user['id']
    order.status = 1
    order.save()
    order.refresh_from_db()
    response = auth_client.get(f"/users/{user['id']}/order")
    assert response.status_code == 200
    assert response.data[0]['coin'] == 10


@pytest.mark.django_db
def test_delete_user_order(user, auth_client):
    order = Order()
    order.id = 1
    order.coin = 10
    order.rewards = 'Starbucks'
    order.qr = '1/jason/jason@gmail.com/2022-01-01/18:00:00'
    order.user_id = user['id']
    order.status = 1
    order.save()
    order.refresh_from_db()
    response = auth_client.put(f"/users/{order.id}/order")
    assert response.status_code == 205


@pytest.mark.django_db
def test_post_user_order(user, auth_client):
    payload = dict(
        id=1,
        coin=10,
        rewards='Starbucks',
        qr='1/jason/jason@gmail.com/2022-01-01/18:00:00',
        user=user['id'],
        status=1,
    )
    response = auth_client.post("/users/addorder", payload)
    assert response.status_code == 201
    order = Order.objects.all().first()
    assert response.data['coin'] == order.coin
