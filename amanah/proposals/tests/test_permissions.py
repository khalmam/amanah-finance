import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_investor_cannot_create_proposal():
    client = APIClient()

    investor = User.objects.create_user(
        username="investor",
        password="pass123",
        role="investor"
    )

    client.force_authenticate(user=investor)

    response = client.post("/api/proposals/", {
        "title": "Test",
        "description": "Desc",
        "capital_required": 100000,
        "duration_months": 6,
        "investor_profit_ratio": 60,
        "entrepreneur_profit_ratio": 40,
    })

    assert response.status_code == 403

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
