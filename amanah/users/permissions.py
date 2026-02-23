from rest_framework.permissions import BasePermission


# ---------- Helpers ----------

def is_admin(user):
    return (
        user.is_authenticated
        and (user.is_superuser or user.role == "admin")
    )


# ---------- Role-based permissions ----------

class IsEntrepreneur(BasePermission):
    """
    Allows entrepreneurs or superusers.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role == "entrepreneur"
                or request.user.is_superuser
            )
        )


class IsInvestor(BasePermission):
    """
    Allows investors or superusers.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role == "investor"
                or request.user.is_superuser
            )
        )


class IsEntrepreneurOrAdmin(BasePermission):
    """
    Allows entrepreneurs, admins, or superusers.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role == "entrepreneur"
                or request.user.role == "admin"
                or request.user.is_superuser
            )
        )


class IsAdmin(BasePermission):
    """
    Allows admins or superusers.
    """
    def has_permission(self, request, view):
        return is_admin(request.user)
        
