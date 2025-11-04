from rest_framework import serializers
from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "parent",
            "subcategories",
        ]
        read_only_fields = ("id", "slug")

    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data
