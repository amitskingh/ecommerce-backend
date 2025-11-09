from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Brand
from ..serializers.brand import BrandSerializer
from ..utils.response_wrapper import success_response, error_response
from ..permissions import ReadOnlyOrAdmin  # assuming you have this permission


class BrandViewSet(ViewSet):
    """ViewSet for Brand model"""

    permission_classes = [ReadOnlyOrAdmin]

    def list(self, request):
        try:
            brands = Brand.objects.all()
            serializer = BrandSerializer(brands, many=True)
            return success_response(
                message="Brands fetched successfully.",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return error_response(
                message="Failed to fetch brands.",
                errors={"detail": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                message="Brand created successfully.",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED,
            )
        return error_response(
            message="Brand creation failed due to validation errors.",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def retrieve(self, request, pk=None):
        brand = get_object_or_404(Brand, pk=pk)
        serializer = BrandSerializer(brand)
        return success_response(
            message="Brand retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def update(self, request, pk=None):
        brand = get_object_or_404(Brand, pk=pk)
        serializer = BrandSerializer(brand, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                message="Brand updated successfully.",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )
        return error_response(
            message="Brand update failed.",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request, pk=None):
        brand = get_object_or_404(Brand, pk=pk)
        brand.delete()
        return success_response(
            message="Brand deleted successfully.",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT,
        )
