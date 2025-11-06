from rest_framework import serializers
from ..models import Cart, CartItem
from .product_variants import ProductVariantSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product_variant",
            "quantity",
            "subtotal",
        ]
        read_only_fields = ["id"]


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "items",
        ]

        read_only_fields = ["id"]


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            "id",
            "cart",
            "product_variant",
            "quantity",
        ]
        read_only_fields = ["id"]
