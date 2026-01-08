from rest_framework.permissions import BasePermission

def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role == "admin")



class IsEntrepreneur(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.role == "entrepreneur" or request.user.is_superuser)
        )


class IsInvestor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.role == "investor" or request.user.is_superuser)
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return is_admin(request.user)


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        # Allow authenticated users to create/list
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            is_admin(request.user) or
            obj.entrepreneur == request.user
        )
