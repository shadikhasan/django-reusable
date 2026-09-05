from typing import Any

import stripe
from django.conf import settings

from .base import PaymentWebhookHandler


class StripeWebhookHandler(PaymentWebhookHandler):
    """Handle Stripe webhook events."""

    def verify(
        self,
        payload: bytes,
        headers: dict[str, str],
    ) -> Any:
        """
        Verify a Stripe webhook signature.

        Args:
            payload: Raw Stripe webhook request body.
            headers: HTTP request headers.

        Returns:
            Verified Stripe event.

        Raises:
            ValueError: If the Stripe signature is missing or invalid.
        """
        signature = headers.get("Stripe-Signature")

        if not signature:
            raise ValueError("Missing Stripe-Signature header.")

        try:
            return stripe.Webhook.construct_event(
                payload,
                signature,
                settings.STRIPE_WEBHOOK_SECRET,
            )
        except (ValueError, stripe.error.SignatureVerificationError) as exc:
            raise ValueError(
                "Invalid Stripe webhook signature or payload."
            ) from exc

    def handle(
        self,
        event: Any,
    ) -> Any:
        """
        Handle a verified Stripe webhook event.

        Args:
            event: Verified Stripe event.

        Returns:
            Stripe event data.
        """
        return event.data.object