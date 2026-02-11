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




class IsInvestorOrOwnerOrAdmin(BasePermission):
    """
    Authentication-level access only.
    Role filtering MUST happen in queryset.
    """

    def has_permission(self, request, view):
        # Just check authentication - nothing else!
        return request.user.is_authenticated  # ← Fixed this line

    def has_object_permission(self, request, view, obj):
        user = request.user
        role = getattr(user, 'role', None)

        if user.is_superuser or role == 'admin':
            return True
        if role == 'investor' and obj.status == 'approved':
            return True
        if role == 'entrepreneur' and obj.entrepreneur == user:
            return True
        return False


class IsModeratorOrAdmin(BasePermission):
    """
    Only moderators and admins can approve proposals
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            (request.user.role in ['moderator', 'admin'] or request.user.is_superuser)
        )