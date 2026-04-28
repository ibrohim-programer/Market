from rest_framework.permissions import BasePermission

class Seller(BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_seller)
    
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and request.user.is_seller)

class Customer(BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_customer)
    
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and request.user.is_customer)
    
class IsOwner(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and obj.user == request.user)