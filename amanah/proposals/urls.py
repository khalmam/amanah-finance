from django.urls import path
from .views import ProposalCreateView, ProposalListView, ProposalApproveView, ProposalRejectView, AuthTestView, MarkInterestView, RemoveInterestView, MyInterestedProposalsView, ModeratorProposalListView

urlpatterns = [
    path('', ProposalCreateView.as_view()),
    path('list/', ProposalListView.as_view()),
    path('<int:pk>/approve/', ProposalApproveView.as_view()),
    path('<int:pk>/reject/', ProposalRejectView.as_view()),
    path("auth-test/", AuthTestView.as_view()),

# Moderator endpoints
    path('moderator/all/', ModeratorProposalListView.as_view(), name='moderator-proposal-list'),  # ← Add
    path('<int:pk>/approve/', ProposalApproveView.as_view(), name='proposal-approve'),
    path('<int:pk>/reject/', ProposalRejectView.as_view(), name='proposal-reject'),

# Investor interest endpoints
    path('<int:pk>/mark-interest/', MarkInterestView.as_view(), name='mark-interest'),  # ← Add
    path('<int:pk>/remove-interest/', RemoveInterestView.as_view(), name='remove-interest'),  # ← Add
    path('my-interests/', MyInterestedProposalsView.as_view(), name='my-interests'),  # ← Add
    

]
