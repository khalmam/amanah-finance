import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_entrepreneur_can_create_proposal():
    client = APIClient()
    # Create user
    entrepreneur = User.objects.create_user(username="test_ent", password="password")
    # Manually set and save to be 100% sure it's in the DB
    entrepreneur.role = "entrepreneur"
    entrepreneur.save()

    client.force_authenticate(user=entrepreneur)

    response = client.post("/api/proposals/", {
        "title": "Halal Poultry",
        "description": "Farm business",
        "capital_required": 200000,
        "duration_months": 12,
        "investor_profit_ratio": 60,
        "entrepreneur_profit_ratio": 40,
    })

    # If it fails, this print will show you the exact error from Django
    if response.status_code != 201:
        print(f"Error Details: {response.data}")
    
    assert response.status_code == 201

@pytest.mark.django_db
def test_entrepreneur_can_create_proposal():
    client = APIClient()

    entrepreneur = User.objects.create_user(
        username="entrepreneur",
        password="pass123",
        role="entrepreneur"
    )

    client.force_authenticate(user=entrepreneur)

    response = client.post("/api/proposals/", {
        "title": "Halal Poultry",
        "description": "Farm business",
        "capital_required": 200000,
        "duration_months": 12,
        "investor_profit_ratio": 60,
        "entrepreneur_profit_ratio": 40,
    })

    assert response.status_code == 201
