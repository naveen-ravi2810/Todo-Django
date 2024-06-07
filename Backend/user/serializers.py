from rest_framework import serializers
from .models import Users


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["first_name", "last_name", "password", "email", "phone"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["first_name", "last_name", "last_logged_in", "email", "phone"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
