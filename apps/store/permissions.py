from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Shop,Category,Product,ProductImage,ProductVariant

class Get_AllowAny_Other_IsAuthenticated(BasePermission):
    """
    GET/HEAD/OPTIONS : allowed for everyone
    PUT/PATCH/DELETE : only for shop owner who owns the object

    Public: 
        GET : list all data
    Authenticated: 
        - Customer: 
            Get : Allow 
        -Shop Owner:
            GET : list only own data
            PUT/PATCH/DELETE : Allow
    """
    
    def has_permission(self, request, view):
        # Public 
        user = request.user
        if request.method in SAFE_METHODS:
            return True
        
        # Customer Can access only for get, 
        if user and user.is_authenticated and user.role == 'customer' and request.method in SAFE_METHODS:
            return True     
        
        # Other methods require authentication
        # For Anonymous user cant access POST,PUT,PACTH,DELETE,HEAD
        return request.user and request.user.is_authenticated and request.user.role == 'shop_owner'
    
 