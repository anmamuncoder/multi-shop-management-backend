from rest_framework.permissions import BasePermission, SAFE_METHODS

class CustomShopPermission(BasePermission):
    """
    GET: Allow For AllowAny
    is_authenticated: POST,PUT,PATCH,HEAD ALL
    is_anonymous: All Method Block except GET
    """
    def has_permission(self, request, view):
        # Allow GET for anyone
        user = request.user

        # Any user allow GET
        if request.method == "GET":
            return True
        
        # For Anonymous user cant access POST,PUT,PACTH,DELETE,HEAD
        if user.is_anonymous:
            return False
        
        # Other methods require authentication
        return request.user and request.user.is_authenticated
