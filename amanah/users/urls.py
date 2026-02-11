from django.urls import path
from .views import RegisterView
from .views import EntrepreneurSignupView, InvestorSignupView, TestAuthView

urlpatterns = [
    path('signup/entrepreneur/', EntrepreneurSignupView.as_view(), name='signup-entrepreneur'),
    path('signup/investor/', InvestorSignupView.as_view(), name='signup-investor'),
    # path('register/', RegisterView.as_view(), name='register'),
    # Add to urls.py
    path('test-auth/', TestAuthView.as_view()),

]


