import json
from typing import Any

import requests
from django.conf import settings

from .base import PaymentWebhookHandler


class PayPalWebhookHandler(PaymentWebhookHandler):
    """Handle PayPal webhook events."""

    def __init__(self):
        """Initialize the PayPal webhook handler."""
        self.base_url = (
            "https://api-m.sandbox.paypal.com"
            if settings.PAYPAL_ENVIRONMENT == "sandbox"
            else "https://api-m.paypal.com"
        )

    def verify(
        self,
        payload: bytes,
        headers: dict[str, str],
    ) -> Any:
        """
        Verify a PayPal webhook signature.

        Args:
            payload: Raw PayPal webhook request body.
            headers: PayPal webhook headers.

        Returns:
            Verified PayPal webhook event.
        """
        event = json.loads(payload)

        response = requests.post(
            f"{self.base_url}/v1/notifications/verify-webhook-signature",
            headers={
                "Authorization": f"Bearer {self._get_access_token()}",
                "Content-Type": "application/json",
            },
            json={
                "auth_algo": headers["PAYPAL-AUTH-ALGO"],
                "cert_url": headers["PAYPAL-CERT-URL"],
                "transmission_id": headers["PAYPAL-TRANSMISSION-ID"],
                "transmission_sig": headers["PAYPAL-TRANSMISSION-SIG"],
                "transmission_time": headers["PAYPAL-TRANSMISSION-TIME"],
                "webhook_id": settings.PAYPAL_WEBHOOK_ID,
                "webhook_event": event,
            },
            timeout=10,
        )

        response.raise_for_status()

        if response.json()["verification_status"] != "SUCCESS":
            raise ValueError("Invalid PayPal webhook signature.")

        return event

    def handle(self, event: Any) -> Any:
        """
        Handle a verified PayPal webhook event.

        Args:
            event: Verified PayPal webhook event.

        Returns:
            PayPal webhook event.
        """
        return event

    def _get_access_token(self) -> str:
        """Get a PayPal OAuth access token."""
        response = requests.post(
            f"{self.base_url}/v1/oauth2/token",
            auth=(
                settings.PAYPAL_CLIENT_ID,
                settings.PAYPAL_CLIENT_SECRET,
            ),
            data={"grant_type": "client_credentials"},
            timeout=10,
        )

        response.raise_for_status()

        return response.json()["access_token"]