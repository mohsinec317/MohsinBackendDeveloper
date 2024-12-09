import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test GraphQL query
def test_graphql_get_trips():
    query = """
    query {
      getTrips(limit: 5, offset: 0) {
        trips {
          id
          vendorId
          passengerCount
          pickupLongitude
          pickupLatitude
          pickupDatetime
          dropoffDatetime
          tripDuration
        }
      }
    }
    """
    response = client.post(
        "/graphql",
        json={"query": query}
    )
    assert response.status_code == 200
    data = response.json()["data"]["getTrips"]
    assert len(data["trips"]) <= 5
    assert "id" in data["trips"][0]

# Invalid parameters test
def test_graphql_get_trips_invalid_parameters():
    query = """
    query {
      getTrips(limit: -5, offset: 0) {
        trips {
          id
        }
      }
    }
    """
    response = client.post(
        "/graphql",
        json={"query": query}
    )
    assert response.status_code == 400
    assert "errors" in response.json()

# No data test
def test_graphql_get_trips_no_data():
    query = """
    query {
      getTrips(limit: 5, offset: 0) {
        trips {
          id
        }
      }
    }
    """
    response = client.post(
        "/graphql",
        json={"query": query}
    )
    assert response.status_code == 200
    data = response.json()["data"]["getTrips"]
    assert len(data["trips"]) == 0
