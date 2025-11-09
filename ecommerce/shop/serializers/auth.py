from rest_framework import serializers
from ..models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(required=False, default="customer")

    class Meta:
        model = User
        fields = ["email", "password", "role", "first_name", "last_name"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data.get("role", "customer"),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
