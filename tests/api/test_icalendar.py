import pytest


@pytest.mark.django_db
def test_post_iCal_url_201(user, auth_client):
    payload = dict(
        user=user['id'],
        icsUrl='https://www.abdn.ac.uk/mytimetable/subscribe/myical/a476233af75af0450a857b367d6b7e5ec46207bd7b0b8a0422e345e049a806b7/1647978491'
    )
    response = auth_client.post('/icalurl', payload)
    assert response.status_code == 201
