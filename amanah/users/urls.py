from django.urls import path
from .views import RegisterView
from .views import EntrepreneurSignupView, InvestorSignupView, TestAuthView, ModeratorSignupView

urlpatterns = [
    path('signup/entrepreneur/', EntrepreneurSignupView.as_view(), name='signup-entrepreneur'),
    path('signup/investor/', InvestorSignupView.as_view(), name='signup-investor'),
    path('signup/moderator/', ModeratorSignupView.as_view(), name='signup-moderator'), 
    path('test-auth/', TestAuthView.as_view()),

]


