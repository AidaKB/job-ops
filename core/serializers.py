from rest_framework import serializers
from . import models


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=255)
    password2 = serializers.CharField(write_only=True, max_length=255)

    class Meta:
        model = models.CustomUser
        fields = ('id', 'username', 'password', 'password2', 'first_name', 'last_name', 'email', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'Password and password confirmation do not match.'
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        role = validated_data.get('role')

        if role == 'admin':
            user = models.CustomUser.objects.create_superuser(
                username=validated_data.pop('username'),
                password=password,
                **validated_data
            )
        else:
            user = models.CustomUser.objects.create_user(
                username=validated_data.pop('username'),
                password=password,
                **validated_data
            )

        return user

    def update(self, instance, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)  # هش کردن پسورد
        instance.save()
        return instance
