from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission.
    Assumes object has `entrepreneur` field.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser
            or getattr(obj, "entrepreneur", None) == request.user
        )

# class IsInvestorOrOwnerOrAdmin(BasePermission):
#     """
#     Allows:
#     - investors to see approved proposals
#     - entrepreneurs to see their own proposals
#     - admins to see all
#     """

#     def has_permission(self, request, view):
#         return request.user.is_authenticated

#     def has_object_permission(self, request, view, obj):
#         user = request.user
#         if user.role == 'admin' or user.is_superuser:
#             return True
#         if user.role == 'investor' and obj.status == 'approved':
#             return True
#         if user.role == 'entrepreneur' and obj.entrepreneur == user:
#             return True
#         return False

# class IsInvestorOrOwnerOrAdmin(BasePermission):
#     def has_permission(self, request, view):
#         # 1. User must be logged in
#         if not request.user.is_authenticated:
#             return False
        
#         # 2. Check if the user has a valid role to even enter the list view
#         # This ensures only admins, investors, or entrepreneurs can call this API
#         return hasattr(request.user, 'role') and request.user.role in ['investor', 'entrepreneur', 'admin']

#     def has_object_permission(self, request, view, obj):
#         user = request.user
#         if user.is_superuser or user.role == 'admin':
#             return True
#         if user.role == 'investor' and obj.status == 'approved':
#             return True
#         if user.role == 'entrepreneur' and obj.entrepreneur == user:
#             return True
#         return False


class IsInvestorOrOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        # 1. Check if user is even logged in
        if not (request.user and request.user.is_authenticated):
            return False
        
        # 2. IMPORTANT: For the LIST view, we check the role globally.
        # Use getattr to prevent errors if the 'role' field is missing.
        user_role = getattr(request.user, 'role', None)
        
        # Allow access to the view if they have one of the valid roles
        return user_role in ['investor', 'entrepreneur', 'admin'] or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        # This part handles individual items (GET /api/proposals/1/)
        user = request.user
        user_role = getattr(user, 'role', None)

        if user.is_superuser or user_role == 'admin':
            return True
        if user_role == 'investor' and obj.status == 'approved':
            return True
        if user_role == 'entrepreneur' and obj.entrepreneur == user:
            return True
        return False