from rest_framework import permissions


class IsAllowedToModifyJobTask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_admin():
            return True
        elif user.is_sales():
            return obj.job.created_by == user
        elif user.is_technician():
            if view.action in ['destroy']:
                return False
            return obj.job.assigned_to == user
        return False
