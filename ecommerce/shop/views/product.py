from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from ..models import Product, ProductImage
from ..serializers.product import (
    ProductListSerializer,
    ProductSerializer,
    ProductDetailSerializer,
    ProductImageSerializer,
)


from ..permissions import IsAdminUser

from ..utils.response_wrapper import success_response, error_response


class ProductListView(APIView):
    """View to list all products"""

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == "GET":
            # Allow anyone to read
            self.permission_classes = [AllowAny]
        elif self.request.method == "POST":
            # Only authenticated users can create
            self.permission_classes = [IsAdminUser]
        else:
            # Only admin users for other methods (PUT, DELETE, etc.)
            self.permission_classes = [IsAdminUser]

        return [permission() for permission in self.permission_classes]

    def get(self, request):
        # authorization_header = request.headers.get("Authorization")
        # print(authorization_header)

        print(request.user.role)

        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        print(request.user.role)

        serializer = ProductSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """View to retrieve, update, or delete a product"""

    def get_permissions(self):

        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
        elif self.request.method == "PATCH":
            self.permission_classes = [IsAdminUser]
        elif self.request.method == "DELETE":
            self.permission_classes = [IsAdminUser]
        return [permission() for permission in self.permission_classes]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductImageView(APIView):
    """View to upload product images"""

    permission_classes = [AllowAny]

    def post(self, request, product_id):
        product = Product.objects.filter(pk=product_id).first()
        if not product:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductImageSerializer(
            data=request.data, context={"product": product_id}
        )

        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id, image_id):

        try:
            product = get_object_or_404(Product, pk=product_id)
            image = get_object_or_404(ProductImage, product.images.all(), pk=image_id)

            if product.created_by == request.user:
                image.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"error": "You are not authorized to delete this image"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except Exception as e:
            return Response(
                {"error": "An error occurred while deleting the image"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
