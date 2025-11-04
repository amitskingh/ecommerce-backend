from rest_framework import serializers
from ..models import ProductVariant


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "name",
            "price",
            "stock",
            "sku",
        ]

        read_only_fields = ["id"]
