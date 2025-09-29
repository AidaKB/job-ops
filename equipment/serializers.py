from rest_framework import serializers
from . import models


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Equipment
        fields = "__all__"
