import pytest

from api.models import Recommendation


@pytest.mark.django_db
def test_get_all_recommend(user, auth_client):
    recommend = Recommendation()
    recommend.id = 1
    recommend.name = 'Mopup Coffee'
    recommend.coin = 20
    recommend.save()
    recommend.refresh_from_db()
    response = auth_client.get('/recommend')
    assert response.status_code == 200
    # assert first data
    assert response.data[0]['coin'] == 20


@pytest.mark.django_db
def test_post_recommend(user, auth_client):
    payload = dict(
        id=1,
        name='Mopup Coffee',
        coin=20,
    )
    response = auth_client.post('/recommend', payload)
    assert response.status_code == 201
    # get data from db after post and compare with response data
    recommend_from_db = Recommendation.objects.all().first()
    assert response.data['coin'] == recommend_from_db.coin


@pytest.mark.django_db
def test_get_one_recommend(user, auth_client):
    recommend = Recommendation()
    recommend.id = 1
    recommend.name = 'Mopup Coffee'
    recommend.coin = 20
    recommend.save()
    recommend.refresh_from_db()
    response = auth_client.get(f"/recommend/{recommend.id}")
    assert response.status_code == 200
    # assert first data
    assert response.data['coin'] == 20
