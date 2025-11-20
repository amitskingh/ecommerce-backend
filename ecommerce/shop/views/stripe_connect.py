from rest_framework.views import APIView
from rest_framework.response import Response
from ..permissions import IsSellerUser
from ..models import User


import stripe

from decouple import config


class StripeConnectAccount(APIView):

    permission_classes = [IsSellerUser]

    def get(self, request, format=None):
        """
        Generates and returns a new account link for an existing Stripe account.
        """
        user = request.user
        stripe.api_key = config("stripe_api_key")

        if not user.stripe_account_id:
            return Response(
                {"error": "Stripe account not found for this user."}, status=404
            )

        try:
            account_link = stripe.AccountLink.create(
                account=user.stripe_account_id,
                refresh_url="https://dashboard.stripe.com/workbench/blueprints/learn-accounts-v1-marketplace/create-account-step?confirmation-redirect=createAccountLink",
                return_url="https://dashboard.stripe.com/workbench/blueprints/learn-accounts-v1-marketplace/create-account-step?confirmation-redirect=createAccountLink",
                type="account_onboarding",
            )
            return Response({"account_link": account_link}, status=200)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=400)

    def post(self, request, format=None):

        user = request.user

        stripe.api_key = config("stripe_api_key")

        print(stripe.api_key)

        email = user.email
        name = user.first_name + " " + user.last_name

        print("INSIDE")

        try:
            account = stripe.Account.create(
                business_profile={"name": name},
                email=email,
                country="us",
                controller={
                    "losses": {"payments": "application"},
                    "stripe_dashboard": {"type": "express"},
                    "fees": {"payer": "application"},
                    "requirement_collection": "stripe",
                },
            )

            account_link = stripe.AccountLink.create(
                account=account.id,
                refresh_url="https://dashboard.stripe.com/workbench/blueprints/learn-accounts-v1-marketplace/create-account-step?confirmation-redirect=createAccountLink",
                return_url="https://dashboard.stripe.com/workbench/blueprints/learn-accounts-v1-marketplace/create-account-step?confirmation-redirect=createAccountLink",
                type="account_onboarding",
            )

            # Save the Stripe account ID to the user model
            if account and account.id:
                user.stripe_account_id = account.id
                user.save()

            return Response(
                {
                    "account": account,
                    "account link": account_link,
                },
                status=200,
            )
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=400)
