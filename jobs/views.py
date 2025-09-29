from rest_framework import generics
from . import models
from .serializers import JobSerializer, TechnicianJobUpdateSerializer, JobTaskSerializer
from core.permissions import IsAdminOrSalesForCreate
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions
from .permissions import IsAllowedToModifyJobTask


class JobListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAdminOrSalesForCreate]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return models.Job.objects.all()
        elif user.is_sales():
            return models.Job.objects.filter(created_by=user)
        elif user.is_technician():
            return models.Job.objects.filter(assigned_to=user)
        return models.Job.objects.none()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class JobDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Job.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return models.Job.objects.all()
        elif user.is_sales():
            return models.Job.objects.filter(created_by=user)
        elif user.is_technician():
            return models.Job.objects.filter(assigned_to=user)
        return models.Job.objects.none()

    def get_serializer_class(self):
        user = self.request.user
        if self.request.method in ['PUT', 'PATCH']:
            if user.is_technician():
                return TechnicianJobUpdateSerializer
        return JobSerializer

    def perform_update(self, serializer):
        user = self.request.user
        instance = self.get_object()

        if user.is_admin():
            serializer.save()
        elif user.is_sales():
            if instance.created_by != user:
                raise PermissionDenied("You can only update jobs you created.")
            if 'status' in serializer.validated_data:
                raise PermissionDenied("Sales agents are not allowed to update status.")
            serializer.save()
        elif user.is_technician():
            if instance.assigned_to != user:
                raise PermissionDenied("You can only update jobs assigned to you.")
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update this job.")

    def perform_destroy(self, instance):
        user = self.request.user
        if user.is_admin():
            instance.delete()
        elif user.is_sales():
            if instance.created_by == user:
                instance.delete()
            else:
                raise PermissionDenied("You can only delete jobs you created.")
        elif user.is_technician():
            raise PermissionDenied("Technicians are not allowed to delete jobs.")
        else:
            raise PermissionDenied("You do not have permission to delete this job.")


class JobTaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = JobTaskSerializer
    permission_classes = [IsAdminOrSalesForCreate]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return models.JobTask.objects.all()
        elif user.is_sales():
            return models.JobTask.objects.filter(job__created_by=user)
        elif user.is_technician():
            return models.JobTask.objects.filter(job__assigned_to=user)
        return models.JobTask.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_admin() or user.is_sales():
            serializer.save()
        else:
            raise PermissionDenied("Only admins and sales agents can create job tasks.")


class JobTaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = JobTaskSerializer
    permission_classes = [IsAdminOrSalesForCreate]

    def get_queryset(self):
        user = self.request.user
        qs = models.JobTask.objects.select_related('job').prefetch_related('required_equipment')
        if user.is_admin():
            return qs.all()
        elif user.is_sales():
            return qs.filter(job__created_by=user)
        elif user.is_technician():
            return qs.filter(job__assigned_to=user)
        return qs.none()


class JobTaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobTaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAllowedToModifyJobTask]

    def get_queryset(self):
        user = self.request.user
        qs = models.JobTask.objects.select_related('job').prefetch_related('required_equipment')
        if user.is_admin():
            return qs.all()
        elif user.is_sales():
            return qs.filter(job__created_by=user)
        elif user.is_technician():
            return qs.filter(job__assigned_to=user)
        return qs.none()

    def perform_update(self, serializer):
        user = self.request.user
        instance = self.get_object()

        if user.is_admin():
            serializer.save()
        elif user.is_sales():
            if instance.job.created_by != user:
                raise PermissionDenied("You can only update tasks for jobs you created.")
            serializer.save()
        elif user.is_technician():
            if instance.job.assigned_to != user:
                raise PermissionDenied("You can only update tasks assigned to you.")
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update this task.")

    def perform_destroy(self, instance):
        user = self.request.user
        if user.is_admin():
            instance.delete()
        elif user.is_sales():
            if instance.job.created_by == user:
                instance.delete()
            else:
                raise PermissionDenied("You can only delete tasks for jobs you created.")
        elif user.is_technician():
            raise PermissionDenied("Technicians are not allowed to delete tasks.")
        else:
            raise PermissionDenied("You do not have permission to delete this task.")
