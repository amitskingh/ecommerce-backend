from rest_framework import serializers
from ..models import Category


# Used for create/update (no recursion, simpler)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "parent",
        ]
        read_only_fields = ("id", "slug")


# Used for retrieval/list (includes nested subcategories)
class CategoryListSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

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
        # Fetch all subcategories of this category
        sub_cats = obj.subcategories.all()
        # Recursively serialize subcategories using the same serializer
        return CategoryListSerializer(sub_cats, many=True).data
