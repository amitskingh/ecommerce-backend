import stripe
import logging

from decouple import config

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import User, Fine

logger = logging.getLogger(__name__)

# This is your test secret API key.
# This is your test secret API key.
stripe.api_key = config("stripe_api_key")
# Replace this endpoint secret with your endpoint's unique secret
# If you are testing with the CLI, find the secret by running 'stripe listen'
# If you are using an endpoint defined with the API or dashboard, look in your webhook settings
# at https://dashboard.stripe.com/webhooks
endpoint_secret = config("whsecret_key")


# @app.route("/webhook", methods=["POST"])
class StripeWebhookView(APIView):
    """
    Stripe webhook view to handle various events.
    """

    permission_classes = [AllowAny]  # Webhooks must be publicly accessible

    def post(self, request, format=None):
        # Use request.body to get the raw, unparsed payload for signature verification
        payload = request.body
        sig_header = request.headers.get("stripe-signature")
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            # Invalid payload
            logger.warning(f"Webhook error while parsing payload: {e}")
            return Response(
                {"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST
            )
        except stripe.SignatureVerificationError as e:
            # Invalid signature
            logger.warning(f"Webhook signature verification failed: {e}")
            return Response(
                {"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Handle the event
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            logger.info(f"Checkout session {session.id} was successful!")
            print(session)
            self.handle_checkout_session(session)

        elif event["type"] == "account.updated":
            account = event["data"]["object"]
            logger.info(f"Stripe Connect account {account.id} was updated.")
            self.handle_account_updated(account)

        else:
            # Unexpected event type
            logger.info("Unhandled event type {}".format(event["type"]))

        # Return a 200 response to acknowledge receipt of the event
        return Response({"status": "success"}, status=status.HTTP_200_OK)

    def handle_checkout_session(self, session):
        """
        Handles the logic for a completed checkout session.
        """
        # Log the metadata from the completed checkout session
        logger.info(f"Checkout session metadata: {session.metadata}")

        payment_intent_id = session.get("payment_intent")

        # Example: Check metadata to see if this was a fine payment
        if session.metadata.get("payment_for") == "fine":
            fine_id = session.metadata.get("fine_id")
            if not fine_id:
                logger.error(
                    "`fine_id` not found in session metadata for fine payment."
                )
                return

            try:
                fine = Fine.objects.get(id=fine_id)

                # Idempotency check: ensure we haven't processed this before
                if fine.payment_intent_id == payment_intent_id:
                    logger.info(
                        f"Fine {fine_id} has already been processed for payment intent {payment_intent_id}."
                    )
                    return

                if fine.status != "paid":
                    fine.status = "paid"
                    fine.payment_intent_id = payment_intent_id
                    fine.save()
                    logger.info(f"Fine {fine_id} marked as paid.")
                else:
                    logger.warning(
                        f"Fine {fine_id} was already marked as paid, but with a different payment intent."
                    )
            except Fine.DoesNotExist:
                logger.error(
                    f"Fine with id={fine_id} not found for completed checkout session."
                )

    def handle_account_updated(self, account):
        """
        Handles updates to a connected Stripe account.
        """
        try:
            user = User.objects.get(stripe_account_id=account.id)
            user.charges_enabled = account.charges_enabled
            user.payouts_enabled = account.payouts_enabled
            user.details_submitted = account.details_submitted
            # Convert StripeObjects to dicts before saving to JSONField
            user.requirements = (
                account.requirements.to_dict_recursive() if account.requirements else {}
            )
            user.capabilities = (
                account.capabilities.to_dict_recursive() if account.capabilities else {}
            )
            user.save()
            logger.info(f"Updated user {user.email} with Stripe account status.")
        except User.DoesNotExist:
            logger.error(
                f"Received account.updated webhook for non-existent user with stripe_account_id={account.id}"
            )
