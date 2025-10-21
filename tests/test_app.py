import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_read_activities():
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities

def test_signup_for_activity():
    """Test signing up for an activity"""
    email = "test@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]

    # Verify the student was added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

def test_signup_duplicate():
    """Test signing up a student who is already registered"""
    email = "michael@mergington.edu"  # Using existing participant from data
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity():
    """Test signing up for an activity that doesn't exist"""
    response = client.post("/activities/NonexistentClub/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_unregister_from_activity():
    """Test unregistering from an activity"""
    # First sign up a test user
    email = "testunregister@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Now unregister them
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]

    # Verify the student was removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]

def test_unregister_not_registered():
    """Test unregistering a student who isn't registered"""
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]