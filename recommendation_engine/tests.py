import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_set_recommendation_strategy(setup_data):
    client = setup_data["client_admin"]

    # Test setting recommendation strategy to location-based
    url = reverse("set_recommendation_strategy")
    response = client.post(url, data={"strategy": "location"})
    assert response.status_code == 200
    assert response.json()["message"] == "Global recommendation strategy set to 'location'."

@pytest.mark.django_db
def test_set_recommendation_strategy_invalid(setup_data):
    client = setup_data["client_admin"]

    # Test invalid recommendation strategy
    url = reverse("set_recommendation_strategy")
    response = client.post(url, data={"strategy": "invalid_strategy"})
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid strategy name. Valid options are: location, trending."

@pytest.mark.django_db
def test_set_recommendation_strategy_trending(setup_data):
    client = setup_data["client_admin"]

    # Test setting recommendation strategy to trending-based
    url = reverse("set_recommendation_strategy")
    response = client.post(url, data={"strategy": "trending"})
    assert response.status_code == 200
    assert response.json()["message"] == "Global recommendation strategy set to 'trending'."

@pytest.mark.django_db
def test_set_recommendation_strategy_location(setup_data):
    client = setup_data["client_admin"]

    # Test setting recommendation strategy to trending-based
    url = reverse("set_recommendation_strategy")
    response = client.post(url, data={"strategy": "location"})
    assert response.status_code == 200
    assert response.json()["message"] == "Global recommendation strategy set to 'location'."

@pytest.mark.django_db
def test_get_recommendations_location_based(setup_data):
    client = setup_data["client_admin"]

    # Set recommendation strategy to location-based
    url = reverse("set_recommendation_strategy")
    client.post(url, data={"strategy": "location"})

    # Test getting recommendations with location-based strategy
    recommendation_url = reverse("get_recommendations")
    response = client.get(recommendation_url, data={"location": "Limerick"})
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_recommendations_trending_based(setup_data):
    client = setup_data["client_admin"]

    # Set recommendation strategy to trending-based
    url = reverse("set_recommendation_strategy")
    client.post(url, data={"strategy": "trending"})

    # Test getting recommendations with trending-based strategy
    recommendation_url = reverse("get_recommendations")
    response = client.get(recommendation_url)
    assert response.status_code == 200