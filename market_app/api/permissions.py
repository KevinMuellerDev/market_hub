from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django.contrib.auth.models import AnonymousUser
class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request,view):
        is_staff = bool(request.user and request.user.is_staff)
        return is_staff or request.method in SAFE_METHODS
    
# permission abfrage anhand des usernames
class IsNiels(BasePermission):
    def has_permission(self, request, view):
        is_niels = bool(request.user and request.user.username == 'Niels')
        return is_niels
    
class IsAdminForDeleteOrPatchAndReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method =="DELETE":
            return bool(request.user and request.user.is_superuser)
        else:
            return bool(request.user and request.user.is_staff)
        
class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == "DELETE":
            return bool(request.user and request.user.is_superuser)    
        else:
            print(obj.user_id)
            return request.user and (request.user.id == obj.user_id or request.user.is_superuser)
