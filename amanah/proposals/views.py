from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import BusinessProposal
from .serializers import BusinessProposalSerializer
from .permissions import IsEntrepreneur, IsInvestor, IsAdmin

class ProposalCreateView(generics.CreateAPIView):
    serializer_class = BusinessProposalSerializer
    permission_classes = [permissions.IsAuthenticated, IsEntrepreneur, IsAdmin]

    def perform_create(self, serializer):
        serializer.save(entrepreneur=self.request.user)


class ProposalListView(generics.ListAPIView):
    serializer_class = BusinessProposalSerializer
    permission_classes = [permissions.IsAuthenticated, IsInvestor, IsAdmin]

    def get_queryset(self):
        return BusinessProposal.objects.filter(status='pending')


class ProposalApproveView(generics.UpdateAPIView):
    queryset = BusinessProposal.objects.all()
    serializer_class = BusinessProposalSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def perform_update(self, serializer):
        serializer.save(status='approved')

class ProposalRejectView(generics.UpdateAPIView):
    queryset = BusinessProposal.objects.all()
    serializer_class = BusinessProposalSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def perform_update(self, serializer):
        serializer.save(status='rejected')