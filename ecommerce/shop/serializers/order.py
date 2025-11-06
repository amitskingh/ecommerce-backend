from rest_framework import serializers
from ..models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "address",
            "total_amount",
            "discount",
            "grand_total",
            "payment_status",
            "order_status",
            "created_at",
            "approved_by",
        ]
        read_only_fields = ["id"]
