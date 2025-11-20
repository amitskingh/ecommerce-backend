from django.urls import path
from ..views.payment import (
    PaymentProcessor,
    FineProcessor,
    FinePaymentSuccess,
    FinePaymentCancel,
)
from ..views.webhook import StripeWebhookView
from ..views.stripe_connect import StripeConnectAccount


# urlpatterns = [
#     path(
#         "payment/",
#         PaymentProcessor.as_view(),
#         name="register_user",
#     ),
#     path(
#         "webhook/",
#         StripeWebhookView.as_view(),
#         name="register_user",
#     ),
#     path(
#         "create-account/",
#         StripeConnectAccount.as_view(),
#         name="create_account",
#     ),
# ]


urlpatterns = [
    path(
        "webhook/",
        StripeWebhookView.as_view(),
        name="stripe_webhook",
    ),
    path(
        "create-account/",
        StripeConnectAccount.as_view(),
        name="create_account",
    ),
    path(
        "fines/<int:pk>/pay/",
        FineProcessor.as_view(),
        name="pay_fine",
    ),
    path(
        "fines/<int:pk>/success/",
        FinePaymentSuccess.as_view(),
        name="fine_payment_success",
    ),
    path(
        "fines/<int:pk>/cancel/",
        FinePaymentCancel.as_view(),
        name="fine_payment_cancel",
    ),
]
