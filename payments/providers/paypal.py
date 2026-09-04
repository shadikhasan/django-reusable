from typing import Any

from django.conf import settings
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import (
    OrdersCaptureRequest,
    OrdersCreateRequest,
    OrdersGetRequest,
)
from paypalcheckoutsdk.payments import CapturesRefundRequest

from .base import PaymentProvider


class PayPalProvider(PaymentProvider):
    """Payment provider using the PayPal Checkout API."""

    def __init__(self):
        """Initialize the PayPal client with the configured credentials."""
        environment = SandboxEnvironment(
            client_id=settings.PAYPAL_CLIENT_ID,
            client_secret=settings.PAYPAL_CLIENT_SECRET,
        )
        self.client = PayPalHttpClient(environment)

    def create_payment(
        self,
        amount: int,
        currency: str,
        **kwargs: Any,
    ) -> Any:
        """
        Create a PayPal order.

        Args:
            amount: Payment amount in the smallest currency unit.
            currency: Three-letter ISO 4217 currency code.
            **kwargs: Additional PayPal order options.

        Returns:
            PayPal order response.
        """
        request = OrdersCreateRequest()

        request.prefer("return=representation")
        request.request_body(
            {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": currency.upper(),
                            "value": f"{amount / 100:.2f}",
                        }
                    }
                ],
                **kwargs,
            }
        )

        return self.client.execute(request).result

    def get_payment(self, payment_id: str) -> Any:
        """
        Retrieve a PayPal order.

        Args:
            payment_id: PayPal order identifier.

        Returns:
            PayPal order response.
        """
        request = OrdersGetRequest(payment_id)

        return self.client.execute(request).result

    def capture_payment(
        self,
        payment_id: str,
        **kwargs: Any,
    ) -> Any:
        """
        Capture a PayPal order.

        Args:
            payment_id: PayPal order identifier.
            **kwargs: Additional PayPal capture options.

        Returns:
            PayPal capture response.
        """
        request = OrdersCaptureRequest(payment_id)

        request.prefer("return=representation")

        if kwargs:
            request.request_body(kwargs)

        return self.client.execute(request).result

    def refund_payment(
        self,
        payment_id: str,
        amount: int | None = None,
        currency: str | None = None,
        **kwargs: Any,
    ) -> Any:
        """
        Refund a captured PayPal payment.

        Args:
            payment_id: PayPal capture identifier.
            amount: Optional refund amount in the smallest currency unit.
                If omitted, the full captured payment is refunded.
            currency: Three-letter ISO 4217 currency code. Required when
                a partial refund amount is provided.
            **kwargs: Additional PayPal refund options.

        Returns:
            PayPal refund response.

        Raises:
            ValueError: If a partial refund is requested without currency.
        """
        if amount is not None and currency is None:
            raise ValueError(
                "Currency is required for a partial PayPal refund."
            )

        request = CapturesRefundRequest(payment_id)

        if amount is not None or kwargs:
            body = {
                **kwargs,
            }

            if amount is not None:
                body["amount"] = {
                    "value": f"{amount / 100:.2f}",
                    "currency_code": currency.upper(),
                }

            request.request_body(body)

        return self.client.execute(request).result