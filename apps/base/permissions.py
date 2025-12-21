from rest_framework.permissions import BasePermission

class IsShopOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or user.is_anonymous:
            return False
        
        return user and user.role == 'shop_owner'

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or user.is_anonymous:
            return False
        
        return user and user.role == 'customer'

class ShopOwnerReadPatch(BasePermission):
    """
    Custom permission:
    - Customers: full access to their order items
    - Shop owners: can only GET or PATCH their order items
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.role == "customer":
            return True  

        if user.role == "shop_owner":
            return request.method in ['GET', 'PATCH']  

        return False

class ShopOwnerRead(BasePermission):
    """
    Custom permission: 
    - Shop owners: can only GET 
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.role == "customer":
            return True  

        if user.role == "shop_owner":
            return request.method in ['GET']  

        return False