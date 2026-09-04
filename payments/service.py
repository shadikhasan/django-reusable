from typing import Any

from django.conf import settings

from .providers.base import PaymentProvider
from .providers.paypal import PayPalProvider
from .providers.stripe import StripeProvider


PROVIDERS: dict[str, type[PaymentProvider]] = {
    "stripe": StripeProvider,
    "paypal": PayPalProvider,
}


class PaymentService:
    """High-level service for processing payments."""

    def __init__(self):
        """Initialize the configured payment provider."""
        provider_class = PROVIDERS.get(settings.PAYMENT_PROVIDER)

        if provider_class is None:
            raise ValueError(
                f"Unsupported payment provider: {settings.PAYMENT_PROVIDER}"
            )

        self.provider = provider_class()

    def create(
        self,
        amount: int,
        currency: str,
        **kwargs: Any,
    ) -> Any:
        """
        Create a payment using the configured provider.

        Args:
            amount: Payment amount in the smallest currency unit.
            currency: Three-letter ISO 4217 currency code.
            **kwargs: Provider-specific options.

        Returns:
            Provider-specific payment information.
        """
        return self.provider.create_payment(
            amount=amount,
            currency=currency,
            **kwargs,
        )

    def get(self, payment_id: str) -> Any:
        """
        Retrieve a payment using the configured provider.

        Args:
            payment_id: Provider payment identifier.

        Returns:
            Provider-specific payment information.
        """
        return self.provider.get_payment(payment_id)

    def capture(
        self,
        payment_id: str,
        **kwargs: Any,
    ) -> Any:
        """
        Capture an authorized payment.

        Args:
            payment_id: Provider payment identifier.
            **kwargs: Provider-specific options.

        Returns:
            Provider-specific payment information.
        """
        return self.provider.capture_payment(
            payment_id=payment_id,
            **kwargs,
        )

    def refund(
        self,
        payment_id: str,
        amount: int | None = None,
        **kwargs: Any,
    ) -> Any:
        """
        Refund a payment.

        Args:
            payment_id: Provider payment or capture identifier.
            amount: Optional refund amount in the smallest currency unit.
            **kwargs: Provider-specific options.

        Returns:
            Provider-specific refund information.
        """
        return self.provider.refund_payment(
            payment_id=payment_id,
            amount=amount,
            **kwargs,
        )