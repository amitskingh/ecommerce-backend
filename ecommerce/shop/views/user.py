from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers.user import UserStripeAccountUpdateSerializer
from ..utils.response_wrapper import success_response, error_response


class UserStripeAccountUpdateView(APIView):
    """
    Update the Stripe account ID for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UserStripeAccountUpdateSerializer(
            user, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return success_response(
                message="Stripe account ID updated successfully.",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )

        return error_response(
            message="Failed to update Stripe account ID.",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
