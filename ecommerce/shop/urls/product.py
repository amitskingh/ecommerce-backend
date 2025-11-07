from django.urls import path
from django.urls import path
from django.urls import path
from ..views.product import (
    ProductListView,
    ProductDetailView,
    ProductImageUploadView,
)

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path(
        "products/<int:pk>/images/",
        ProductImageUploadView.as_view(),
        name="product_image",
    ),
]
