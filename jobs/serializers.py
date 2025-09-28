from rest_framework import serializers
from . import models


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
