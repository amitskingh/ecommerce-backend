from rest_framework import serializers
from ..models import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "product_variant",
            "quantity",
            "price",
        ]

        read_only_fields = ["id"]
