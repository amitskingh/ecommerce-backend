from rest_framework.permissions import BasePermission, SAFE_METHODS


# 🧑‍💼 Admin-only access
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


# 🧑‍🔧 Seller-only access
class IsSellerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "seller"


# 🧑‍🤝‍🧑 Customer-only access
class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "customer"


# ✅ Admin or Seller access
class IsAdminOrSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            "admin",
            "seller",
        ]


# 👀 Read-only for everyone, but write access for admin/seller
class ReadOnlyOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user.is_authenticated and request.user.role in [
            "admin",
        ]


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
