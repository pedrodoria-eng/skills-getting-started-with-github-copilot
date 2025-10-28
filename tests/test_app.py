from urllib.parse import quote

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # basic sanity: one known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "testuser@example.com"

    # ensure email not present
    resp = client.get("/activities")
    assert resp.status_code == 200
    participants = resp.json()[activity]["participants"]
    assert email not in participants

    # sign up (use URL-encoded activity name)
    signup_path = f"/activities/{quote(activity)}/signup"
    resp = client.post(signup_path, params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # confirm present
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert email in participants

    # unregister
    unregister_path = f"/activities/{quote(activity)}/unregister"
    resp = client.post(unregister_path, params={"email": email})
    assert resp.status_code == 200
    assert "Unregistered" in resp.json().get("message", "")

    # confirm removed
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert email not in participants
