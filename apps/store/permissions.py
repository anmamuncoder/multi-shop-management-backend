from rest_framework.permissions import BasePermission, SAFE_METHODS

class Get_AllowAny_Other_IsAuthenticated(BasePermission):
    """
    GET/HEAD/OPTIONS : allowed for everyone
    PUT/PATCH/DELETE : only for shop owner who owns the object

    Public: 
        GET : list all data
    Authenticated: 
        GET : list only own data
        PUT/PATCH/DELETE : Allow
    """
    
    def has_permission(self, request, view):
        # Public 
        if request.method in SAFE_METHODS:
            return True

        # Other methods require authentication
        # For Anonymous user cant access POST,PUT,PACTH,DELETE,HEAD
        return request.user and request.user.is_authenticated
    
    # def has_object_permission(self, request, view, obj):
        # pass