from rest_framework import serializers
from . import models
from equipment.serializers import EquipmentSerializer


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Job
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request:
            if request.user.is_sales() and request.method in ['PUT', 'PATCH']:
                self.fields.pop('status', None)


class TechnicianJobUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Job
        fields = ['status']


class JobTaskSerializer(serializers.ModelSerializer):
    required_equipment = EquipmentSerializer(many=True, read_only=False)

    class Meta:
        model = models.JobTask
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'completed_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request:
            user = request.user
            method = request.method

            if method in ['PUT', 'PATCH']:
                if user.is_sales():
                    if 'status' in self.fields:
                        self.fields.pop('status')
                elif user.is_technician():
                    allowed_fields = ['status', 'required_equipment']
                    for field_name in list(self.fields.keys()):
                        if field_name not in allowed_fields + ['id', 'job', 'created_at', 'updated_at', 'completed_at']:
                            self.fields.pop(field_name)

    def update(self, instance, validated_data):
        equipment_data = validated_data.pop('required_equipment', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if equipment_data is not None:
            instance.required_equipment.set([e['id'] if isinstance(e, dict) else e for e in equipment_data])
        return instance
