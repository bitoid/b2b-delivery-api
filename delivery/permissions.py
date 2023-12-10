from rest_framework import permissions

class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'client')

class IsCourier(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'courier')
