import pytest

from api.models import UserICal, Coins


@pytest.mark.django_db
def test_get_lectures(user, auth_client):
    iCal = UserICal()
    iCal.id = 1
    iCal.summary = 'Practical'
    iCal.date = '2022-01-01'
    iCal.start = '12:00:00'
    iCal.end = '14:00:00'
    iCal.location = 'Online'
    iCal.status = 0
    iCal.user_id = user['id']
    iCal.icsName = 'Personal Timetable'
    iCal.save()
    iCal.refresh_from_db()
    response = auth_client.get(f"/lectures/{user['id']}/{iCal.date}")

    assert response.status_code == 200


@pytest.mark.django_db
def test_put_lectures(user, auth_client):
    iCal = UserICal()
    iCal.id = 1
    iCal.summary = 'Practical'
    iCal.date = '2022-01-01'
    iCal.start = '12:00:00'
    iCal.end = '14:00:00'
    iCal.location = 'Online'
    iCal.status = 0
    iCal.user_id = user['id']
    iCal.icsName = 'Personal Timetable'
    iCal.save()
    iCal.refresh_from_db()
    # crete one coin for testing
    coin = Coins()
    coin.id = 1
    coin.user_id = user['id']
    coin.coin = 0
    coin.save()
    coin.refresh_from_db()
    response = auth_client.put(f"/users/lectures/{iCal.id}")
    assert response.status_code == 205
    iCal.refresh_from_db()
    newICal = UserICal.objects.all().first()
    assert newICal.status == 1
