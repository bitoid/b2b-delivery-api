from rest_framework import permissions

class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'client') and obj.client.user == request.user:
            return True
        if hasattr(request.user, 'courier') and obj.courier.user == request.user:
            return True
        return False
    
class IsClientOrSuperuser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        return hasattr(request.user, 'client')
    

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsCourierForPostOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return hasattr(request.user, 'courier')
        return False