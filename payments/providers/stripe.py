from typing import Any

import stripe
from django.conf import settings

from .base import PaymentProvider


class StripeProvider(PaymentProvider):
    """Payment provider using the Stripe API."""

    def __init__(self):
        """Initialize Stripe with the configured API key."""
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def create_payment(
        self,
        amount: int,
        currency: str,
        **kwargs: Any,
    ) -> Any:
        """
        Create a payment through Stripe.

        Args:
            amount: Payment amount in the smallest currency unit.
            currency: Three-letter ISO 4217 currency code.
            **kwargs: Additional Stripe payment options.

        Returns:
            Stripe PaymentIntent object.
        """
        return stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            **kwargs,
        )

    def get_payment(self, payment_id: str) -> Any:
        """
        Retrieve a payment from Stripe.

        Args:
            payment_id: Stripe PaymentIntent identifier.

        Returns:
            Stripe PaymentIntent object.
        """
        return stripe.PaymentIntent.retrieve(payment_id)

    def capture_payment(
        self,
        payment_id: str,
        **kwargs: Any,
    ) -> Any:
        """
        Capture an authorized Stripe payment.

        Args:
            payment_id: Stripe PaymentIntent identifier.
            **kwargs: Additional Stripe capture options.

        Returns:
            Stripe PaymentIntent object.
        """
        return stripe.PaymentIntent.capture(
            payment_id,
            **kwargs,
        )

    def cancel_payment(
        self,
        payment_id: str,
        **kwargs: Any,
    ) -> Any:
        """
        Cancel an authorized Stripe payment.

        Args:
            payment_id: Stripe PaymentIntent identifier.
            **kwargs: Additional Stripe cancellation options.

        Returns:
            Stripe PaymentIntent object.
        """
        return stripe.PaymentIntent.cancel(
            payment_id,
            **kwargs,
        )

    def refund_payment(
        self,
        payment_id: str,
        amount: int | None = None,
        **kwargs: Any,
    ) -> Any:
        """
        Refund a Stripe payment.

        Args:
            payment_id: Stripe PaymentIntent identifier.
            amount: Optional refund amount in the smallest currency unit.
                If omitted, the full payment is refunded.
            **kwargs: Additional Stripe refund options.

        Returns:
            Stripe Refund object.
        """
        params = {
            "payment_intent": payment_id,
            **kwargs,
        }

        if amount is not None:
            params["amount"] = amount

        return stripe.Refund.create(**params)