from django.urls import path, include
from ..views.brand import BrandViewSet
from rest_framework.routers import DefaultRouter


# Create router instance
router = DefaultRouter()

# Register the BrandViewSet
router.register(r"brands", BrandViewSet, basename="brand")

urlpatterns = [
    path("", include(router.urls)),
]
