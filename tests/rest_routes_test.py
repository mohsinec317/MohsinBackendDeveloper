import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test GET /trips/ endpoint
def test_get_trips_valid():
    response = client.get("/trips/", params={"limit": 5, "offset": 0})
    assert response.status_code == 200
    assert "trips" in response.json()
    assert isinstance(response.json()["trips"], list)

def test_get_trips_limit_exceeded():
    response = client.get("/trips/", params={"limit": 200, "offset": 0})
    assert response.status_code == 400
    assert response.json()["detail"] == "Limit cannot exceed 100 records"

def test_get_trips_no_data():
    response = client.get("/trips/", params={"limit": 5, "offset": 0})
    assert response.status_code == 404
    assert response.json()["detail"] == "No trips found"

# Test POST /trips/summary endpoint
def test_post_trips_summary_date():
    data = {"type": "date_summary", "limit": 10}
    response = client.post("/trips/summary", json=data)
    assert response.status_code == 200
    assert "status" in response.json() and response.json()["status"] == 1

def test_post_trips_summary_invalid_type():
    data = {"type": "invalid_summary_type"}
    response = client.post("/trips/summary", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid summary type"
