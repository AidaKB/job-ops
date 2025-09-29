from rest_framework import generics
from . import models
from .serializers import EquipmentListSerializer
from .permissions import CanUpdateOrDeleteEquipment
from core.permissions import IsAdminOrSalesForCreate


class EquipmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Equipment.objects.all()
    serializer_class = EquipmentListSerializer
    permission_classes = [IsAdminOrSalesForCreate]


class EquipmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Equipment.objects.all()
    serializer_class = EquipmentListSerializer
    permission_classes = [CanUpdateOrDeleteEquipment]
