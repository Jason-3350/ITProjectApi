import pytest

from api.models import Notices


@pytest.mark.django_db
def test_get_notice(user, auth_client):
    add_notice = Notices()
    add_notice.notice = 'Welcome'
    add_notice.user_id = user['id']
    add_notice.save()
    add_notice.refresh_from_db()
    response = auth_client.get(f"/notice/{user['id']}")
    assert response.status_code == 200
    added_notice = Notices.objects.all().first()
    assert len(response.data) == 1
    assert response.data[0]['notice'] == added_notice.notice
