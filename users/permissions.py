from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Permission class to allow only Admin users"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "Admin"

class IsDoctor(permissions.BasePermission):
    """Permission class to allow only Doctor users"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "Doctor"

class IsUser(permissions.BasePermission):
    """Permission class to allow only Regular Users"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "User"
