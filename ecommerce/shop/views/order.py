from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..models import OrderItem, Cart, Order

from ..serializers.cart import CartItemSerializer
from ..serializers.order_item import OrderItemSerializer
from ..serializers.order import OrderSerializer


class OrderView(ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):

        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        items = Cart.objects.get(user=request.user).items.all()

        # serilizers = OrderSerializer(data=request.data, partial=True)
        # if serilizers.is_valid():
        #     serilizers.save()

        order = Order.objects.create(
            user=request.user,
            address=request.data.get("address"),
        )

        total_price = 0

        for item in items:
            data = {
                "order": order.id,
                "product_variant": item.product_variant,
                "quantity": item.quantity,
                "price": item.subtotal,
            }

            total_price += item.subtotal

            serilizers = OrderItemSerializer(data=data)
            if serilizers.is_valid():
                serilizers.save()
            else:
                return Response(serilizers.errors, status=status.HTTP_400_BAD_REQUEST)

        order.total_amount = total_price
        order.grand_total = total_price
        order.save()

    def retrieve(self, request, pk=None):
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        order = Order.objects.get(pk=pk)

        order_status = request.data.get("order_status")
        order_approved_by = request.user

        if order_status:
            order.order_status = order_status

        if order_approved_by:
            order.approved_by = order_approved_by

        order.save()

        serializer = OrderSerializer(order)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
