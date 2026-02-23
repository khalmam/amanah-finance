from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .serializers import UserSerializer, EntrepreneurSignupSerializer, InvestorSignupSerializer, ModeratorSignupSerializer
from .models import User


# Add this to users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class TestAuthView(APIView):
    # No authentication_classes, no permission_classes - purely global
    
    def get(self, request):
        return Response({
            'user': str(request.user),
            'authenticated': request.user.is_authenticated
        })

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Entrepreneur signup
class EntrepreneurSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = EntrepreneurSignupSerializer

    def perform_create(self, serializer):
        serializer.save(role='entrepreneur')

# Investor signup
class InvestorSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = InvestorSignupSerializer

    def perform_create(self, serializer):
        serializer.save(role='investor')


class ModeratorSignupView(generics.CreateAPIView):
    """
    Register a new moderator account.
    Only admins can create moderator accounts for security.
    """
    serializer_class = ModeratorSignupSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins can create moderators