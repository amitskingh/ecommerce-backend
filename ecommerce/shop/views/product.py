from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from ..models import Product
from ..serializers.product import (
    ProductSerializer,
    ProductCreateSerializer,
    ProductDetailSerializer,
    ProductImageSerializer,
)


from ..permissions import IsSuperAdminUser, IsAdminUser


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
            self.permission_classes = [IsAdminUser | IsSuperAdminUser]
        else:
            # Only admin users for other methods (PUT, DELETE, etc.)
            self.permission_classes = [IsSuperAdminUser]

        return [permission() for permission in self.permission_classes]

    def get(self, request):
        # authorization_header = request.headers.get("Authorization")
        # print(authorization_header)

        print(request.user.role)

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        print(request.user.role)

        serializer = ProductCreateSerializer(
            data=request.data, context={"request": request}
        )
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
            self.permission_classes = [IsSuperAdminUser | IsAdminUser]
        elif self.request.method == "DELETE":
            self.permission_classes = [IsSuperAdminUser | IsAdminUser]
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


class ProductImageUploadView(APIView):
    """View to upload product images"""

    permission_classes = [AllowAny]

    def post(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductImageSerializer(data=request.data, context={"product": pk})

        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
