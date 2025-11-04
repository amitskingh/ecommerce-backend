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
                ],  # Added a comma here
                mode="payment",
                success_url=YOUR_DOMAIN + "?success=true",
                cancel_url=YOUR_DOMAIN + "?canceled=true",
            )

        except Exception as e:
            return str(e)

        return Response({"url: ": checkout_session.url})
