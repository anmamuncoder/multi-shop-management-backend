from rest_framework.permissions import BasePermission, SAFE_METHODS


class GETOwnerAllCustomer(BasePermission):
    """
    Shop Owner: Read-only access (SAFE_METHODS only)
    Customer: Full access (GET, POST, PUT, PATCH, DELETE)
    """

    def has_permission(self, request, view):
        user = request.user

        # Must be authenticated
        if not user or not user.is_authenticated:
            return False

        # Customer: allow all methods
        if user.role == "customer":
            return True

        # Owner: allow GET only
        if user.role == "shop_owner" and request.method in SAFE_METHODS:
            return True

        return False
    
    