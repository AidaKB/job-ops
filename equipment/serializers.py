from rest_framework import serializers
from . import models


class EquipmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = models.Equipment
        fields = ['id', 'name', 'type', 'serial_number', 'is_active']