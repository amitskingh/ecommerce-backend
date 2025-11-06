from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..serializers.discount import DiscountSerializer
from ..models import Discount


class DiscountListView(APIView):
    """View to list all discounts"""

    permission_classes = [AllowAny]

    def get(self, request):
        discounts = Discount.objects.all()
        serializer = DiscountSerializer(discounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DiscountSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
