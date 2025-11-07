from rest_framework import serializers
from ..models import Product

from .product_variants import ProductVariantSerializer


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "brand",
            "base_price",
            "stock",
            "is_active",
        ]
        read_only_fields = ["id"]


class ProductDetailSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "brand",
            "base_price",
            "stock",
            "is_active",
            "variants",
        ]
        read_only_fields = ["id"]


class ProductCreateSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "brand",
            "base_price",
            "stock",
            "is_active",
            "created_by",
        ]
        read_only_fields = ["id"]


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "id",
            "product",
            "image_url",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        product = self.context["product"]
        validated_data["product"] = product
        return super().create(validated_data)
