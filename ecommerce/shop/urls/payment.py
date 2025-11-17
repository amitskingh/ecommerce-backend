from django.urls import path
from ..views.payment import PaymentProcessor
from ..views.webhook import StripeWebhookView
from ..views.stripe_connect import StripeConnectAccount


urlpatterns = [
    path(
        "payment/",
        PaymentProcessor.as_view(),
        name="register_user",
    ),
    path(
        "webhook/",
        StripeWebhookView.as_view(),
        name="register_user",
    ),
    path(
        "create-account/",
        StripeConnectAccount.as_view(),
        name="create_account",
    ),
]
