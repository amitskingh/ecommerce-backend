from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from decouple import config

import stripe

stripe.api_key = config("stripe_api_key")

YOUR_DOMAIN = "http://127.0.0.1:8000/"


class PaymentProcessor(APIView):
    def post(self, request, format=None):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": "Subscription Plan A",
                                "description": "Monthly access to premium features",
                            },
                            "unit_amount": 2000,  # $20.00
                        },
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url=YOUR_DOMAIN + "?success=true",
                cancel_url=YOUR_DOMAIN + "?canceled=true",
                metadata={
                    "product_name": "Subscription Plan A",
                    "product_description": "Monthly access to premium features",
                },
            )

            # ✅ Proper DRF Response
            return Response({"url": checkout_session.url}, status=status.HTTP_200_OK)

        except Exception as e:
            # ✅ Also return a proper Response here
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
