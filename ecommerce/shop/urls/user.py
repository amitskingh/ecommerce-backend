from django.urls import path
from ..views.user import UserStripeAccountUpdateView

urlpatterns = [
    path(
        "profile/stripe-account/",
        UserStripeAccountUpdateView.as_view(),
        name="user_stripe_account_update",
    ),
]