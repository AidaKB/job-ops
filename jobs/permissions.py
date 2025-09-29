from rest_framework import permissions


class IsAllowedToModifyJobTask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_admin():
            return True
        elif user.is_sales():
            return obj.job.created_by == user
        elif user.is_technician():
            if request.method == 'DELETE':
                return False
            return obj.job.assigned_to == user
        return False


class IsTechnician(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_technician())
