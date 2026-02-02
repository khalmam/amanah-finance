from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import UserSerializer, EntrepreneurSignupSerializer, InvestorSignupSerializer
from .models import User

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