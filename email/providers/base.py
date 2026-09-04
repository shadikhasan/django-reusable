from abc import ABC, abstractmethod
from typing import Sequence


class EmailProvider(ABC):
    """Base interface for email providers."""

    @abstractmethod
    def send(
        self,
        subject: str,
        to: str | Sequence[str],
        message: str,
        html_message: str | None = None,
        from_email: str | None = None,
        attachments: Sequence[tuple] | None = None,
    ) -> int:
        """
        Send an email.

        Args:
            subject: Email subject.
            to: Recipient email address or a sequence of addresses.
            message: Plain-text email body.
            html_message: Optional HTML email body.
            from_email: Optional sender email address.
            attachments: Optional sequence of Django attachment tuples.
                Each tuple should contain:
                (filename, content, mimetype).

        Returns:
            Number of successfully delivered messages.
        """
        raise NotImplementedError