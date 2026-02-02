from django.shortcuts import render


from rest_framework import generics, permissions
from .models import BusinessProposal
from .serializers import BusinessProposalSerializer
from users.permissions import (
    IsEntrepreneur,
    IsInvestor,
    IsEntrepreneurOrAdmin,
)

from utils.permissions import IsOwnerOrAdmin, IsInvestorOrOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.utils import timezone


class ProposalCreateView(generics.CreateAPIView):
    """
    Submit a new Mudarabah business proposal.
    Only entrepreneurs can access this endpoint.
    """
    serializer_class = BusinessProposalSerializer
    permission_classes = [IsEntrepreneurOrAdmin]

    def perform_create(self, serializer):
        serializer.save(entrepreneur=self.request.user)


# views.py

class ProposalListView(generics.ListAPIView):
    serializer_class = BusinessProposalSerializer
    authentication_classes = [JWTAuthentication]   # 🔥 THIS WAS MISSING
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        print(f"--- DEBUG LOG ---")
        print(f"User: {user} | Authenticated: {user.is_authenticated} | Role: {getattr(user, 'role', 'No Role')}")

        if not user.is_authenticated:
            return BusinessProposal.objects.none()

        role = getattr(user, 'role', None)
        if role == 'investor':
            return BusinessProposal.objects.filter(status='approved')
        if role == 'entrepreneur':
            return BusinessProposal.objects.filter(entrepreneur=user)

        return BusinessProposal.objects.all()



class ProposalApproveView(generics.UpdateAPIView):
    queryset = BusinessProposal.objects.filter(status='pending')
    serializer_class = BusinessProposalSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def perform_update(self, serializer):
        serializer.save(
            status='approved',
            approved_by=self.request.user,
            approved_at=timezone.now()
        )

class ProposalRejectView(generics.UpdateAPIView):
    queryset = BusinessProposal.objects.all()
    serializer_class = BusinessProposalSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def perform_update(self, serializer):
        serializer.save(status='rejected')