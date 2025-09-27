from rest_framework import serializers
from . import models
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class CustomLoginSerializer(LoginSerializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError(
                {"detail": "username and password is required"},
                code='authorization'
            )

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError(
                {"detail": "نام کاربری یا رمز عبور نادرست است."},
                code='authorization'
            )

        attrs['user'] = user
        return attrs
