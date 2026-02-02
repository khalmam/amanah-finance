from django.urls import path
from .views import RegisterView
from .views import EntrepreneurSignupView, InvestorSignupView

urlpatterns = [
    path('signup/entrepreneur/', EntrepreneurSignupView.as_view(), name='signup-entrepreneur'),
    path('signup/investor/', InvestorSignupView.as_view(), name='signup-investor'),
    # path('register/', RegisterView.as_view(), name='register'),

]


