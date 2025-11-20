from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from decouple import config
from ..models import Fine
from ..utils.response_wrapper import success_response, error_response


import stripe

stripe.api_key = config("stripe_api_key")

YOUR_DOMAIN = "http://127.0.0.1:8000/api/v1/"


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


class FineProcessor(APIView):

    def post(self, request, pk, format=None):
        try:

            user = request.user

            fine = Fine.objects.filter(pk=pk, user=user).first()

            if not fine:
                return error_response(
                    message="Fine not found or you don't have permission to pay for it.",
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            if fine.status == "paid":
                return error_response(
                    message="This fine has already been paid.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            # Convert amount to cents for Stripe
            amount_in_cents = int(fine.amount * 100)

            account_id = fine.stripe_account_id

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": f"Fine: {fine.name}",
                                "description": f"Fine for {fine.user.email}",
                            },
                            "unit_amount": amount_in_cents,
                        },
                        "quantity": 1,
                    },
                ],
                payment_intent_data={
                    "transfer_data": {
                        "destination": account_id,
                    },
                },
                mode="payment",
                success_url=YOUR_DOMAIN
                + f"fines/{fine.id}/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=YOUR_DOMAIN + f"fines/{fine.id}/cancel",
                metadata={
                    "fine_id": str(fine.id),
                    "user_id": str(user.id),
                    "payment_for": "fine",
                },
            )

            return success_response(
                message="Checkout session created successfully.",
                data={"checkout_url": session.url},
                status_code=status.HTTP_200_OK,
            )

        except Exception as e:
            return error_response(
                message="Failed to create checkout session for fine.",
                errors={"detail": str(e)},
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class FinePaymentSuccess(APIView):
    def get(self, request, pk, format=None):
        session_id = request.query_params.get("session_id")

        if not session_id:
            return error_response(
                message="Session ID is missing.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="Fine payment cancelled.",
            data={"fine_id": pk, "status": "cancelled"},
            status_code=status.HTTP_200_OK,
        )

        # try:
        #     session = stripe.checkout.Session.retrieve(session_id)

        #     if session.payment_status == "paid":
        #         fine = Fine.objects.filter(pk=pk, user=request.user).first()
        #         if fine:
        #             fine.status = "paid"
        #             fine.save()
        #             return success_response(
        #                 message="Fine paid successfully.",
        #                 data={"fine_id": fine.id, "status": fine.status},
        #                 status_code=status.HTTP_200_OK,
        #             )
        #         else:
        #             return error_response(
        #                 message="Fine not found for this user.",
        #                 status_code=status.HTTP_404_NOT_FOUND,
        #             )
        #     else:
        #         return error_response(
        #             message="Payment not successful.",
        #             status_code=status.HTTP_400_BAD_REQUEST,
        #         )

        # except stripe.error.StripeError as e:
        #     return error_response(
        #         message="Stripe error retrieving session.",
        #         errors={"detail": str(e)},
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #     )
        # except Exception as e:
        #     return error_response(
        #         message="An unexpected error occurred.",
        #         errors={"detail": str(e)},
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     )


class FinePaymentCancel(APIView):
    def get(self, request, pk, format=None):
        return success_response(
            message="Fine payment cancelled.",
            data={"fine_id": pk, "status": "cancelled"},
            status_code=status.HTTP_200_OK,
        )
