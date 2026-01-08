from django.urls import path
from .views import ProposalCreateView, ProposalListView, ProposalApproveView, ProposalRejectView

urlpatterns = [
    path('', ProposalCreateView.as_view()),
    path('list/', ProposalListView.as_view()),
    path('<int:pk>/approve/', ProposalApproveView.as_view()),
    path('<int:pk>/reject/', ProposalRejectView.as_view()),
]
