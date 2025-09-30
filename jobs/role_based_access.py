from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet


class RoleQuerysetResolver:
    def get_jobs(self, queryset: QuerySet, user):
        return

    def get_tasks(self, queryset: QuerySet, user):
        return

    def can_update_job(self, user, instance, validated_data):
        return True

    def can_delete_job(self, user, instance):
        return True

    def can_update_task(self, user, instance):
        return True

    def can_delete_task(self, user, instance):
        return True


class AdminResolver(RoleQuerysetResolver):
    def get_jobs(self, queryset: QuerySet, user):
        return queryset.all()

    def get_tasks(self, queryset: QuerySet, user):
        return queryset.all()

    def can_update_job(self, user, instance, validated_data):
        return True

    def can_delete_job(self, user, instance):
        return True


class SalesResolver(RoleQuerysetResolver):
    def get_jobs(self, queryset: QuerySet, user):
        return queryset.filter(created_by=user)

    def get_tasks(self, queryset: QuerySet, user):
        return queryset.filter(job__created_by=user)

    def can_update_job(self, user, instance, validated_data):
        if instance.created_by != user:
            raise PermissionDenied("You can only update jobs you created.")
        if 'status' in validated_data:
            raise PermissionDenied("Sales agents cannot update status.")
        return True

    def can_delete_job(self, user, instance):
        if instance.created_by != user:
            raise PermissionDenied("You can only delete jobs you created.")
        return True


class TechnicianResolver(RoleQuerysetResolver):
    def get_jobs(self, queryset: QuerySet, user):
        return queryset.filter(assigned_to=user)

    def get_tasks(self, queryset: QuerySet, user):
        return queryset.filter(job__assigned_to=user)

    def can_update_job(self, user, instance, validated_data):
        if instance.assigned_to != user:
            raise PermissionDenied("You can only update jobs assigned to you.")
        return True

    def can_delete_job(self, user, instance):
        raise PermissionDenied("Technicians cannot delete jobs.")

    def can_update_task(self, user, instance):
        if instance.job.assigned_to != user:
            raise PermissionDenied("You can only update tasks assigned to you.")
        return True

    def can_delete_task(self, user, instance):
        raise PermissionDenied("Technicians cannot delete tasks.")


def get_role_resolver(user):
    if user.is_admin():
        return AdminResolver()
    elif user.is_sales():
        return SalesResolver()
    elif user.is_technician():
        return TechnicianResolver()
    return RoleQuerysetResolver()  # default: deny all
