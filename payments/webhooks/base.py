from abc import ABC, abstractmethod
from typing import Any


class PaymentWebhookHandler(ABC):
    """Base interface for payment webhook handlers."""

    @abstractmethod
    def verify(
        self,
        payload: bytes,
        headers: dict[str, str],
    ) -> Any:
        """
        Verify a webhook payload.

        Args:
            payload: Raw webhook request body.
            headers: HTTP request headers.

        Returns:
            Verified provider event.
        """
        raise NotImplementedError

    @abstractmethod
    def handle(
        self,
        event: Any,
    ) -> Any:
        """
        Handle a verified webhook event.

        Args:
            event: Verified provider event.

        Returns:
            Provider-specific result.
        """
        raise NotImplementedError