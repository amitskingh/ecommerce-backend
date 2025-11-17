from rest_framework.views import APIView
from rest_framework.response import Response


import stripe

from decouple import config


class StripeConnectAccount(APIView):
    def post(self, request, format=None):

        print(stripe.api_key)

        email = request.data.get("email")
        name = request.data.get("name")

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

            # return Response(
            #     {
            #         "msg": "Account created successfully",
            #         "data": {"name": name, "email": email},
            #     }
            # )
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
