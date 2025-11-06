from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from ..serializers.cart import CartItemSerializer, CartSerializer

from ..models import Cart, CartItem, ProductVariant


class CartViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):

        user_cart = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(user_cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        user_cart, created = Cart.objects.get_or_create(user=request.user)

        product_variant_id = request.data.get("product_variant_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            product_variant = ProductVariant.objects.get(id=product_variant_id)
        except ProductVariant.DoesNotExist:
            return Response(
                {"error": "Product variant not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart_item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            product_variant=product_variant,
            defaults={"quantity": quantity},
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):

        user_cart = Cart.objects.get(user=request.user)

        try:
            cart_item = CartItem.objects.get(id=pk, cart=user_cart)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):

        user_cart = Cart.objects.get(user=request.user)

        if not user_cart:
            return Response(
                {"error": "User cart not found"}, status=status.HTTP_404_NOT
            )

        try:
            cart_item = CartItem.objects.get(id=pk, cart=user_cart)
            quantity = int(request.data.get("quantity"))
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
