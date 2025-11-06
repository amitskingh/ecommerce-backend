from rest_framework import serializers
from ..models import Discount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [
            "id",
            "name",
            "discount_type",
            "value",
            "start_date",
            "end_date",
            "created_by",
            "is_active",
        ]
        read_only_fields = ["id"]
