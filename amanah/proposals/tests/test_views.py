import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from proposals.models import BusinessProposal

User = get_user_model()

@pytest.mark.django_db
def test_only_admin_can_approve_proposal():
    client = APIClient()

    entrepreneur = User.objects.create_user(
        username="ent",
        password="pass123",
        role="entrepreneur"
    )

    investor = User.objects.create_user(
        username="inv",
        password="pass123",
        role="investor"
    )

    proposal = BusinessProposal.objects.create(
        entrepreneur=entrepreneur,
        title="Test",
        description="Desc",
        capital_required=100000,
        duration_months=6,
        investor_profit_ratio=60,
        entrepreneur_profit_ratio=40
    )

    client.force_authenticate(user=investor)
    response = client.patch(f"/api/proposals/{proposal.id}/approve/")

    assert response.status_code == 403

from django.utils import timezone

@pytest.mark.django_db
def test_approval_sets_audit_fields():
    client = APIClient()

    admin = User.objects.create_user(
        username="admin",
        password="pass123",
        role="admin"
    )

    entrepreneur = User.objects.create_user(
        username="ent",
        password="pass123",
        role="entrepreneur"
    )

    proposal = BusinessProposal.objects.create(
        entrepreneur=entrepreneur,
        title="Audit Test",
        description="Desc",
        capital_required=150000,
        duration_months=6,
        investor_profit_ratio=60,
        entrepreneur_profit_ratio=40
    )

    client.force_authenticate(user=admin)
    response = client.patch(f"/api/proposals/{proposal.id}/approve/")

    proposal.refresh_from_db()

    assert response.status_code == 200
    assert proposal.status == "approved"
    assert proposal.approved_by == admin
    assert proposal.approved_at is not None
    assert proposal.approved_at <= timezone.now()


@pytest.mark.django_db
def test_non_pending_proposal_cannot_be_modified():
    client = APIClient()

    admin = User.objects.create_user(
        username="admin2",
        password="pass123",
        role="admin"
    )

    entrepreneur = User.objects.create_user(
        username="ent2",
        password="pass123",
        role="entrepreneur"
    )

    proposal = BusinessProposal.objects.create(
        entrepreneur=entrepreneur,
        title="Locked",
        description="Desc",
        capital_required=120000,
        duration_months=6,
        investor_profit_ratio=60,
        entrepreneur_profit_ratio=40,
        status="approved"
    )

    client.force_authenticate(user=admin)
    response = client.patch(f"/api/proposals/{proposal.id}/approve/")

    assert response.status_code in [400, 404]
