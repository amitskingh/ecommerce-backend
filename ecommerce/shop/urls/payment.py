from django.urls import path
from ..views.payment import PaymentProcessor

urlpatterns = [
    path(
        "payment/",
        PaymentProcessor.as_view(),
        name="register_user",
    ),
]
