from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics, permissions
from .models import BusinessProposal
from .serializers import BusinessProposalSerializer
from users.permissions import (
    IsEntrepreneur,
    IsInvestor,
    IsEntrepreneurOrAdmin,
    
)

from utils.permissions import IsOwnerOrAdmin, IsInvestorOrOwnerOrAdmin,IsModeratorOrAdmin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema


from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

class AuthTestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "user": str(request.user),
            "is_authenticated": request.user.is_authenticated,
            "auth": str(request.auth),
        })



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
    permission_classes = [IsInvestorOrOwnerOrAdmin]
    # NO authentication_classes
    
    def get(self, request, *args, **kwargs):
        print("=" * 50)
        print("USER:", request.user)
        print("AUTHENTICATED:", request.user.is_authenticated)
        print("ROLE:", getattr(request.user, 'role', None))
        print("=" * 50)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        
        print(f"QUERYSET - User: {user}, Role: {role}")
        
        if user.is_superuser or role == 'admin':
            qs = BusinessProposal.objects.all()
        elif role == 'investor':
            qs = BusinessProposal.objects.filter(interested_investors=user)
        elif role == 'entrepreneur':
            qs = BusinessProposal.objects.filter(entrepreneur=user)
        else:
            qs = BusinessProposal.objects.none()
        

        status = self.request.query_params.get('status', None)
        if status:
            qs = qs.filter(status=status)
        
        return qs.order_by('-created_at')
        
        print(f"QUERYSET COUNT: {qs.count()}")
        return qs


class ProposalApproveView(generics.UpdateAPIView):
    """
    Approve a pending proposal.
    """
    queryset = BusinessProposal.objects.filter(status='pending')
    serializer_class = BusinessProposalSerializer
    permission_classes = [IsModeratorOrAdmin]

    def perform_update(self, serializer):
        serializer.save(
            status='approved',
            approved_by=self.request.user,
            approved_at=timezone.now()
        )

class ProposalRejectView(generics.UpdateAPIView):
    """
    Reject a proposal.
    """
    queryset = BusinessProposal.objects.filter(status='pending')
    serializer_class = BusinessProposalSerializer
    permission_classes = [IsModeratorOrAdmin]

    def perform_update(self, serializer):
        serializer.save(status='rejected')


class ModeratorProposalListView(generics.ListAPIView):
    """
    List all pending proposals for moderator review.
    Only moderators and admins can access.
    """
    serializer_class = BusinessProposalSerializer
    permission_classes = [IsModeratorOrAdmin]
    
    def get_queryset(self):
        # Show all proposals, or filter by status via query param
        status = self.request.query_params.get('status', None)
        queryset = BusinessProposal.objects.all()
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')


class MarkInterestView(APIView):
    """
    Investor marks interest in a proposal.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        user = request.user
        
        # Only investors can mark interest
        if getattr(user, 'role', None) != 'investor':
            return Response(
                {'error': 'Only investors can mark interest'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            proposal = BusinessProposal.objects.get(pk=pk, status='approved')
        except BusinessProposal.DoesNotExist:
            return Response(
                {'error': 'Proposal not found or not approved'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Add investor to interested list
        proposal.interested_investors.add(user)
        
        return Response(
            {'message': 'Interest marked successfully'},
            status=status.HTTP_200_OK
        )


class RemoveInterestView(APIView):
    """
    Investor removes interest from a proposal.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, pk):
        user = request.user
        
        if getattr(user, 'role', None) != 'investor':
            return Response(
                {'error': 'Only investors can remove interest'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            proposal = BusinessProposal.objects.get(pk=pk)
        except BusinessProposal.DoesNotExist:
            return Response(
                {'error': 'Proposal not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Remove investor from interested list
        proposal.interested_investors.remove(user)
        
        return Response(
            {'message': 'Interest removed successfully'},
            status=status.HTTP_200_OK
        )


class MyInterestedProposalsView(generics.ListAPIView):
    """
    List all proposals this investor has marked interest in.
    """
    serializer_class = BusinessProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'investor':
            return BusinessProposal.objects.filter(
                status='approved',
                interested_investors=user
            )
        return BusinessProposal.objects.none()