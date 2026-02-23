from rest_framework import serializers
from .models import User



# Core serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

# Entrepreneur-specific serializer
class EntrepreneurSignupSerializer(UserSerializer):
    company_name = serializers.CharField(required=True)
    business_sector = serializers.CharField(required=True)

    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + ['company_name', 'business_sector']

# Investor-specific serializer
class InvestorSignupSerializer(UserSerializer):
    investment_interests = serializers.CharField(required=True)
    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + ['investment_interests']

#Moderator-specific serializer
class ModeratorSignupSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields
    
    def create(self, validated_data):
        validated_data['role'] = 'moderator'  # Force role to moderator
        return super().create(validated_data)
