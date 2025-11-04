from rest_framework import serializers
from ..models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            "id",
            "product_variant",
            "quantity",
            "price",
        ]
        read_only_fields = ["id"]
