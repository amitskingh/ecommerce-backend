from rest_framework.views import APIView

from rest_framework import status

from ..models import Category

from ..serializers.category import CategorySerializer, CategoryListSerializer

from ..permissions import ReadOnlyOrAdmin, IsAdminUser

from ..utils.response_wrapper import success_response, error_response

from django.shortcuts import get_list_or_404, get_object_or_404


class CategoryListView(APIView):
    """View to list all categories"""

    permission_classes = [ReadOnlyOrAdmin]

    def get(self, request):
        categories = Category.objects.filter(parent=None)
        serializer = CategoryListSerializer(categories, many=True)

        return success_response(
            data=serializer.data,
            message="Categories fetched successfully",
            status_code=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return success_response(
                data=serializer.data,
                message="Category created successfully",
                status_code=status.HTTP_201_CREATED,
            )

        return error_response(
            message="Category creation failed",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class CategoryDetailView(APIView):
    """View to retrieve, update, or delete a category"""

    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if not category:

            return error_response(
                message="Category not found",
                errors="Category not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = CategorySerializer(category)

        return success_response(
            data=serializer.data,
            message="Category fetched",
            status_code=status.HTTP_200_OK,
        )

    def patch(self, request, pk):
        category = self.get_object(pk)
        if not category:

            return error_response(
                message="Category not found",
                errors="Category not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return success_response(
                data=serializer.data,
                message="Category updated successfully",
                status_code=status.HTTP_200_OK,
            )

        return error_response(
            message="Category update failed",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return error_response(
                message="Category not found",
                errors="Category not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        category.delete()

        return success_response(
            message="Category deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT,
        )
