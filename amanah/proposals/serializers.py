from rest_framework import serializers
from .models import BusinessProposal


class BusinessProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProposal
        fields = '__all__'
        read_only_fields = ('entrepreneur', 'status')

    def validate(self, data):
        instance = self.instance

        if instance and instance.status != "pending":
            raise serializers.ValidationError(
                "Only pending proposals can be modified."
            )

        investor_ratio = data.get(
            "investor_profit_ratio",
            instance.investor_profit_ratio if instance else None
        )
        entrepreneur_ratio = data.get(
            "entrepreneur_profit_ratio",
            instance.entrepreneur_profit_ratio if instance else None
        )

        if investor_ratio is not None and entrepreneur_ratio is not None:
            if investor_ratio + entrepreneur_ratio != 100:
                raise serializers.ValidationError(
                    "Profit ratios must sum to 100%"
                )

        return data
