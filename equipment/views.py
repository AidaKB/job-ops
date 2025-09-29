from rest_framework import generics
from . import models
from .serializers import EquipmentSerializer
from . import permissions as equipment_permissions
from core.permissions import IsAdminOrSalesForCreate


class EquipmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAdminOrSalesForCreate]


class EquipmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [equipment_permissions.CanUpdateOrDeleteEquipment]
