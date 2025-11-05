from django.urls import path
from ..views.payment import PaymentProcessor
from ..views.webhook import StripeWebhookView

urlpatterns = [
    path(
        "payment/",
        PaymentProcessor.as_view(),
        name="register_user",
    ),
    path(
        "webhook/",
        PaymentProcessor.as_view(),
        name="register_user",
    ),
]
