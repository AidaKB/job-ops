from rest_framework import serializers
from . import models
from equipment.serializers import EquipmentSerializer
from equipment.models import Equipment


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

    def validate(self, data):
        if 'status' in data and data.get('status') == models.Job.Status.COMPLETED:
            job = self.instance or models.Job(**data)
            if not job.all_tasks_completed():
                raise serializers.ValidationError(
                    {"status": "Cannot mark job as completed while some tasks are incomplete."}
                )
        return data


class TechnicianJobUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Job
        fields = ['status']

    def validate(self, data):
        if 'status' in data and data.get('status') == models.Job.Status.COMPLETED:
            job = self.instance or models.Job(**data)
            if not job.all_tasks_completed():
                raise serializers.ValidationError(
                    {"status": "Cannot mark job as completed while some tasks are incomplete."}
                )
        return data


class JobTaskSerializer(serializers.ModelSerializer):
    required_equipment_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Equipment.objects.all(), write_only=True, required=False
    )
    required_equipment = EquipmentSerializer(many=True, read_only=True)

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
                self.fields['required_equipment'] = EquipmentSerializer(
                    many=True, read_only=False
                )
                self.fields.pop('required_equipment_ids', None)

                if user.is_sales():
                    self.fields.pop('status', None)

                elif user.is_technician():
                    allowed_fields = ['status', 'required_equipment']
                    for field_name in list(self.fields.keys()):
                        if field_name not in allowed_fields + [
                            'id', 'created_at', 'updated_at', 'completed_at'
                        ]:
                            self.fields.pop(field_name)

    def create(self, validated_data):
        equipment_ids = validated_data.pop('required_equipment_ids', [])
        job_task = models.JobTask.objects.create(**validated_data)
        if equipment_ids:
            job_task.required_equipment.set(equipment_ids)
        return job_task

    def update(self, instance, validated_data):
        equipment_data = validated_data.pop('required_equipment', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if equipment_data is not None:
            updated_equipment_ids = []
            for eq_data in equipment_data:
                eq_obj = Equipment.objects.get(id=eq_data['id'])
                for attr, value in eq_data.items():
                    if attr != 'id':
                        setattr(eq_obj, attr, value)
                eq_obj.save()
                updated_equipment_ids.append(eq_obj.id)

            instance.required_equipment.set(updated_equipment_ids)

        return instance


class DailyTechnicianLogSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    required_equipment = EquipmentSerializer(many=True, read_only=False)

    class Meta:
        model = models.JobTask
        fields = ['id', 'job_title', 'title', 'description', 'status', 'completed_at', 'required_equipment', 'order',
                  'created_at', 'updated_at']
