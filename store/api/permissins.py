from rest_framework.permissions import BasePermission , SAFE_METHODS
from store.models import Store

class UserVerified(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            request.user.is_verified
        )

class Has_Store(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            Store.objects.get(owner = user)
            return True
        except:
            return False

class IsAdminOrOwnerOrRedonly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and
            request.method in SAFE_METHODS or
            obj.store.owner == request.user or
            request.user.is_staff
        )

# class IsAdminUserORRedonly(BasePermission):
#     def has_permission(self, request, view):
#         return bool(
#             request.user.is_authenticated and
            
#             request.method in SAFE_METHODS or
#             request.user.is_authenticated and
#             request.user.is_staff
#         )
        

class IsAdminOrStoreOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            obj.owner == request.user or
            request.user.is_staff
        )

class IsOrderStoreOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj.store)

        return bool(
            obj.store.owner == request.user or
            request.user.is_staff
        )

class IsAdminOrStoreOwnerForListOrder(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            obj.owner == request.user or
            request.user.is_staff
        ) 