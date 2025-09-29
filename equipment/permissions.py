from rest_framework import permissions


class CanUpdateOrDeleteEquipment(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user.is_authenticated and (
                    request.user.is_admin() or request.user.is_sales()
            )
