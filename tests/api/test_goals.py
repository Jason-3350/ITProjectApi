import pytest

from api.models import Goals, Coins


@pytest.mark.django_db
def test_get_goal(user, auth_client):
    # create two data into database
    goalOne = Goals()
    goalOne.goal = 'Running'
    goalOne.location = 'University'
    goalOne.start = '18:00:00'
    goalOne.end = '19:00:00'
    goalOne.user_id = user['id']
    goalOne.date = '2022-01-01'
    goalOne.save()
    # create one more goal
    goalTwo = Goals()
    goalTwo.goal = 'Running'
    goalTwo.location = 'University'
    goalTwo.start = '18:00:00'
    goalTwo.end = '19:00:00'
    goalTwo.user_id = user['id']
    goalTwo.date = '2022-01-01'
    goalTwo.save()

    response = auth_client.get(f"/goals/{user['id']}/{goalOne.date}")

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_add_goal(user, auth_client):
    addGoal = dict(
        goal='Reading',
        location='Home',
        date='2022-01-01',
        start='18:00:00',
        end='19:00:00',
        status='0',
        user=user['id']
    )
    response = auth_client.post("/users/addgoals", addGoal)
    assert response.status_code == 201
    assert response.data['goal'] == 'Reading'


@pytest.mark.django_db
def test_delete_goal(user, auth_client):
    # create one goal first
    goal = Goals()
    goal.goal = 'Running'
    goal.location = 'University'
    goal.start = '18:00:00'
    goal.end = '19:00:00'
    goal.user_id = user['id']
    goal.date = '2022-01-01'
    goal.status = '0'
    goal.save()

    goal.refresh_from_db()
    response = auth_client.delete(f"/users/goals/{goal.id}")
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_goal_404(user, auth_client):
    response = auth_client.delete("/users/goals/1")
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_goal(user, auth_client):
    # create one goal first
    goal = Goals()
    goal.id = 1
    goal.goal = 'Running'
    goal.location = 'University'
    goal.start = '18:00:00'
    goal.end = '19:00:00'
    goal.user_id = user['id']
    goal.date = '2022-01-01'
    goal.status = '0'
    goal.save()
    # crete one coin for testing
    coin = Coins()
    coin.id = 1
    coin.user_id = user['id']
    coin.coin = 0
    coin.save()
    # refresh the database
    goal.refresh_from_db()
    coin.refresh_from_db()
    response = auth_client.put(f"/users/goals/{goal.id}")
    assert response.status_code == 205


@pytest.mark.django_db
def test_put_goal_404(user, auth_client):
    response = auth_client.put(f"/users/goals/1")
    assert response.status_code == 404
