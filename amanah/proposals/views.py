from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import BusinessProposal
from .serializers import BusinessProposalSerializer
from .permissions import IsEntrepreneur, IsInvestor, IsAdmin, IsEntrepreneurOrAdmin
from django.utils import timezone

# class ProposalCreateView(generics.CreateAPIView):
#     """
#     Submit a new Mudarabah business proposal.
#     Only entrepreneurs can access this endpoint.
#     """
#     serializer_class = BusinessProposalSerializer
#     permission_classes = [permissions.IsAuthenticated, IsEntrepreneur, IsAdmin]

#     def perform_create(self, serializer):
#         serializer.save(entrepreneur=self.request.user)

class ProposalCreateView(generics.CreateAPIView):
    """
    Submit a new Mudarabah business proposal.
    Only entrepreneurs can access this endpoint.
    """
    serializer_class = BusinessProposalSerializer
    permission_classes = [IsEntrepreneurOrAdmin]

    def perform_create(self, serializer):
        serializer.save(entrepreneur=self.request.user)



class ProposalListView(generics.ListAPIView):
    serializer_class = BusinessProposalSerializer
    permission_classes = [permissions.IsAuthenticated, IsInvestor, IsAdmin]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'investor':
            return BusinessProposal.objects.filter(status='approved')
        if user.role == 'entrepreneur':
            return BusinessProposal.objects.filter(entrepreneur=user)
        return BusinessProposal.objects.all()
    


class ProposalApproveView(generics.UpdateAPIView):
    queryset = BusinessProposal.objects.filter(status='pending')
    serializer_class = BusinessProposalSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def perform_update(self, serializer):
        serializer.save(
            status='approved',
            approved_by=self.request.user,
            approved_at=timezone.now()
        )

class ProposalRejectView(generics.UpdateAPIView):
    queryset = BusinessProposal.objects.all()
    serializer_class = BusinessProposalSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def perform_update(self, serializer):
        serializer.save(status='rejected')