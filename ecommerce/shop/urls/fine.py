from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.fine import FineViewSet

# Create router instance
router = DefaultRouter()

# Register the FineViewSet
router.register(r"fines", FineViewSet, basename="fine")

urlpatterns = [
    path("", include(router.urls)),
]
