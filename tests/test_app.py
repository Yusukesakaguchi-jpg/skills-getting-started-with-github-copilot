import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)
ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))


def test_signup_rejects_duplicate_registration():
    activity_name = "Chess Club"
    email = "duplicate@example.com"

    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student is already signed up"


def test_signup_rejects_full_activity():
    activity_name = "Soccer Team"
    max_participants = 24

    for i in range(max_participants):
        email = f"player{i}@example.com"
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200

    response = client.post(f"/activities/{activity_name}/signup?email=overflow@example.com")

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
