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
    