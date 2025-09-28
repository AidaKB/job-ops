from rest_framework import generics
from . import models
from .serializers import JobSerializer, TechnicianJobUpdateSerializer
from . import permissions as jobs_permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions


class JobListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [jobs_permissions.IsAdminOrSalesForCreate]

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
