from abc import ABC, abstractmethod
from typing import Any


class PaymentProvider(ABC):
    """Base interface for payment providers."""

    @abstractmethod
    def create_payment(
        self,
        amount: int,
        currency: str,
        **kwargs: Any,
    ) -> Any:
        """
        Create a payment.

        Args:
            amount: Payment amount in the smallest currency unit.
            currency: Three-letter ISO 4217 currency code.
            **kwargs: Provider-specific options.

        Returns:
            Provider-specific payment information.
        """
        raise NotImplementedError

    @abstractmethod
    def get_payment(self, payment_id: str) -> Any:
        """
        Retrieve a payment.

        Args:
            payment_id: Provider payment or order identifier.

        Returns:
            Provider-specific payment information.
        """
        raise NotImplementedError

    @abstractmethod
    def capture_payment(
        self,
        payment_id: str,
        **kwargs: Any,
    ) -> Any:
        """
        Capture a payment.

        Args:
            payment_id: Provider payment or order identifier.
            **kwargs: Provider-specific options.

        Returns:
            Provider-specific payment information.
        """
        raise NotImplementedError

    @abstractmethod
    def refund_payment(
        self,
        payment_id: str,
        amount: int | None = None,
        currency: str | None = None,
        **kwargs: Any,
    ) -> Any:
        """
        Refund a payment.

        Args:
            payment_id: Provider-specific payment or capture identifier.
            amount: Optional refund amount in the smallest currency unit.
                If omitted, the full remaining amount is refunded.
            currency: Three-letter ISO 4217 currency code. Required when
                a partial refund amount is provided.
            **kwargs: Provider-specific options.

        Returns:
            Provider-specific refund information.
        """
        raise NotImplementedError