import pytest

from api.models import Reward


@pytest.mark.django_db
def test_get_all_recommend(user, auth_client):
    reward = Reward()
    reward.id = 1
    reward.name = 'Starbucks'
    reward.coin = 20
    reward.save()
    reward.refresh_from_db()
    response = auth_client.get('/reward')
    assert response.status_code == 200
    # assert first data
    assert response.data[0]['coin'] == 20


@pytest.mark.django_db
def test_post_recommend(user, auth_client):
    payload = dict(
        id=1,
        name='Starbucks',
        coin=20,
    )
    response = auth_client.post('/reward', payload)
    assert response.status_code == 201
    # get data from db after post and compare with response data
    recommend_from_db = Reward.objects.all().first()
    assert response.data['coin'] == recommend_from_db.coin


@pytest.mark.django_db
def test_get_one_recommend(user, auth_client):
    reward = Reward()
    reward.id = 1
    reward.name = 'Starbucks'
    reward.coin = 20
    reward.save()
    reward.refresh_from_db()
    response = auth_client.get(f"/reward/{reward.id}")
    assert response.status_code == 200
    # assert first data
    assert response.data['coin'] == 20
