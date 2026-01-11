import pytest
from proposals.serializers import BusinessProposalSerializer

@pytest.mark.django_db
def test_profit_ratio_must_equal_100():
    data = {
        "title": "Test Business",
        "description": "Test description",
        "capital_required": 100000,
        "duration_months": 6,
        "investor_profit_ratio": 70,
        "entrepreneur_profit_ratio": 20,  # ❌ total = 90
    }

    serializer = BusinessProposalSerializer(data=data)
    assert not serializer.is_valid()
    assert "Profit ratios must sum to 100%" in str(serializer.errors)
    data["entrepreneur_profit_ratio"] = 30  # ✅ total = 100
    serializer = BusinessProposalSerializer(data=data)
    assert serializer.is_valid()