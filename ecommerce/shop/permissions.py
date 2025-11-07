from rest_framework import permissions


class IsSuperAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "super_admin"
        )


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "user"
        )


class CustomPermissionMixin:
    """
    Mixin to apply different permissions based on user role
    Roles and their permissions:
    - Super Admin: All methods (GET, POST, PUT, PATCH, DELETE)
    - Admin: All methods (GET, POST, PUT, PATCH, DELETE)
    - User: GET, POST, PUT, PATCH (cannot DELETE)
    """

    def get_permissions(self):
        permission_classes = []

        # Check if user is authenticated
        if not self.request.user.is_authenticated:
            return permission_classes

        role = self.request.user.role

        if role == "super_admin":
            permission_classes = [IsSuperAdminUser]
        elif role == "admin":
            permission_classes = [IsAdminUser]
        elif role == "user":
            permission_classes = [IsUser]

        return [permission() for permission in permission_classes]
