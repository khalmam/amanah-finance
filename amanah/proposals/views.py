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
            qs = BusinessProposal.objects.filter(status='approved')
        elif role == 'entrepreneur':
            qs = BusinessProposal.objects.filter(entrepreneur=user)
        else:
            qs = BusinessProposal.objects.none()
        
        print(f"QUERYSET COUNT: {qs.count()}")
        return qs


# class ProposalListView(generics.ListAPIView):
#     serializer_class = BusinessProposalSerializer
#     # We use IsAuthenticated here because the filtering happens in the queryset
#     # authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated] 

#     def get_queryset(self):
#         user = self.request.user
#         role = getattr(user, 'role', None)

#         # DEBUG: Let's see who is asking
#         print(f"Filtering queryset for User: {user.username}, Role: {role}")

#         # 1. Admins see everything
#         if user.is_superuser or role == 'admin':
#             return BusinessProposal.objects.all()
        
#         # 2. Investors see only approved proposals
#         if role == 'investor':
#             return BusinessProposal.objects.filter(status='approved')
        
#         # 3. Entrepreneurs see ONLY their own proposals
#         if role == 'entrepreneur':
#             return BusinessProposal.objects.filter(entrepreneur=user)
            
#         # 4. If no role matches, return nothing (safe default)
#         return BusinessProposal.objects.none()

#     @swagger_auto_schema(security=[{'Bearer': []}])
#     def get(self, request, *args, **kwargs):
#         # --- ADD THESE LINES FOR DEBUGGING ---
#         print("\n" + "="*50)
#         print("DEBUG: Raw Authorization Header:", request.META.get('HTTP_AUTHORIZATION'))
#         print("DEBUG: Request User:", request.user)
#         print("DEBUG: Is Authenticated:", request.user.is_authenticated)
#         # This will list what auth methods Django is trying to use
#         print("DEBUG: Authenticators being used:", [type(a).__name__ for a in request.authenticators])
#         print("="*50 + "\n")
        
#         return super().get(request, *args, **kwargs)





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