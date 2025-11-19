from rest_framework import serializers
from ..models import Fine


class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = ["id", "user", "name", "amount", "created_at"]
        read_only_fields = ["id", "created_at"]
