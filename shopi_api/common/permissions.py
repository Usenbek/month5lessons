from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    def has_permission(self,request, view):
        return request.user.is_authenticated and not request.user.is_staff  


class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsModerator(BasePermission):
    def has_permission(self,request, view):
        if request.user.is_authenticated and request.user.is_staff:
            moderation_methods = ['PUT', 'PATCH', 'DELETE'] + list(SAFE_METHODS)
            return request.method in moderation_methods
        return False
            

    
