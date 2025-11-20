from rest_framework.viewsets import ViewSet
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Fine
from ..serializers.fine import FineSerializer
from ..utils.response_wrapper import success_response, error_response
from ..permissions import ReadOnlyOrAdmin, IsAdminOrSeller


class FineViewSet(ViewSet):
    """ViewSet for Fine model"""

    permission_classes = [IsAdminOrSeller]

    def list(self, request):
        try:
            fines = Fine.objects.all()
            serializer = FineSerializer(fines, many=True)
            return success_response(
                message="Fines fetched successfully.",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return error_response(
                message="Failed to fetch fines.",
                errors={"detail": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        serializer = FineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(stripe_account_id=request.user.stripe_account_id)
            return success_response(
                message="Fine created successfully.",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED,
            )
        return error_response(
            message="Fine creation failed due to validation errors.",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def retrieve(self, request, pk=None):
        fine = get_object_or_404(Fine, pk=pk)
        serializer = FineSerializer(fine)
        return success_response(
            message="Fine retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def update(self, request, pk=None):
        fine = get_object_or_404(Fine, pk=pk)
        serializer = FineSerializer(fine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                message="Fine updated successfully.",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )
        return error_response(
            message="Fine update failed.",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request, pk=None):
        fine = get_object_or_404(Fine, pk=pk)
        fine.delete()
        return success_response(
            message="Fine deleted successfully.",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT,
        )
