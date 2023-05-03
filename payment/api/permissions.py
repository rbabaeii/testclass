from rest_framework.permissions import BasePermission , SAFE_METHODS

class OwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            obj.user == request.user or
            request.user.is_staff
        )

class OrderOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            obj.order.user == request.user or
            request.user.is_staff
        )