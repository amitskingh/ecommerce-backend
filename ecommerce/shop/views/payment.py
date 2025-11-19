from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from decouple import config

import stripe

stripe.api_key = config("stripe_api_key")

YOUR_DOMAIN = "http://127.0.0.1:8000/"


from decouple import config


class PaymentProcessor(APIView):

    def post(self, request, format=None):
        try:

            account_id = config("account_id")

            # payment_intent = stripe.PaymentIntent.create(
            #     amount=2000,
            #     currency="usd",
            #     application_fee_amount=1000,  # Platform cut in cents (e.g., $10.00)
            #     automatic_payment_methods={"enabled": True},
            #     transfer_data={"destination": account_id},
            # )

            # return Response({"url": payment_intent}, status=status.HTTP_200_OK)

            # payment_intent = stripe.PaymentIntent.create(
            #     amount=2000,
            #     currency="usd",
            #     automatic_payment_methods={"enabled": True},
            #     application_fee_amount=1000,  # Platform cut in cents (e.g., $10.00)
            #     line_items=[
            #         {
            #             "price_data": {
            #                 "currency": "usd",
            #                 "product_data": {
            #                     "name": "Subscription Plan A",
            #                     "description": "Monthly access to premium features",
            #                 },
            #                 "unit_amount": 2000,  # $20.00
            #             },
            #             "quantity": 1,
            #         },
            #     ],
            #     mode="payment",
            #     success_url=YOUR_DOMAIN + "?success=true",
            #     cancel_url=YOUR_DOMAIN + "?canceled=true",
            #     metadata={
            #         "product_name": "Subscription Plan A",
            #         "product_description": "Monthly access to premium features",
            #         "destination": account_id,
            #     },
            # )

            # checkout_session = stripe.checkout.Session.create(
            #     line_items=[
            #         {
            #             "price_data": {
            #                 "currency": "usd",
            #                 "product_data": {
            #                     "name": "Subscription Plan A",
            #                     "description": "Monthly access to premium features",
            #                 },
            #                 "unit_amount": 2000,  # $20.00
            #             },
            #             "quantity": 1,
            #         },
            #     ],
            #     mode="payment",
            #     success_url=YOUR_DOMAIN + "?success=true",
            #     cancel_url=YOUR_DOMAIN + "?canceled=true",
            #     metadata={
            #         "product_name": "Subscription Plan A",
            #         "product_description": "Monthly access to premium features",
            #         "destination": account_id,
            #     },
            #     payment_intent=payment_intent.id,
            # )

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": "T-Shirt",
                            },
                            "unit_amount": 250000,  # $2500.00
                        },
                        "quantity": 1,
                    },
                    # Optional: you can add more items here
                ],
                mode="payment",  # or "subscription" if you're selling subscriptions
                payment_intent_data={
                    "application_fee_amount": 30000,  # $300.00 platform fee (in cents)
                    "transfer_data": {
                        "destination": account_id,
                    },
                },
                success_url=YOUR_DOMAIN + "?success=true",
                cancel_url=YOUR_DOMAIN + "?canceled=true",
                metadata={
                    "product_name": "Subscription Plan A",
                    "product_description": "Monthly access to premium features",
                    "destination": account_id,
                },
                # Important for Connect: use stripe_account parameter if you want to create on behalf of the connected account directly
                # stripe_account=CONNECTED_ACCOUNT_ID,  # Uncomment if using "destination charges" (less common now)
            )

            # # ✅ Proper DRF Response
            return Response({"url": session.url}, status=status.HTTP_200_OK)
            # return Response({"url": payment_intent.url}, status=status.HTTP_200_OK)

        except Exception as e:
            # ✅ Also return a proper Response here
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
