from typing import Sequence

from django.conf import settings
from mailgun.client import Client

from .base import EmailProvider


class MailgunProvider(EmailProvider):
    """Email provider using the Mailgun API."""

    def __init__(self):
        """Initialize the Mailgun client with the configured API key."""
        self.client = Client(auth=("api", settings.MAILGUN_API_KEY))

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
        Send an email through Mailgun.

        Args:
            subject: Email subject.
            to: Recipient email address or a sequence of addresses.
            message: Plain-text email body.
            html_message: Optional HTML email body.
            from_email: Optional sender email address. Falls back to
                DEFAULT_FROM_EMAIL when not provided.
            attachments: Optional sequence of Django-style attachment tuples
                in the format (filename, content, mimetype).

        Returns:
            Number of successfully sent messages.
        """
        recipients = [to] if isinstance(to, str) else list(to)
        sender = from_email or settings.DEFAULT_FROM_EMAIL

        # Build the message payload with the required fields.
        data = {
            "from": sender,
            "to": recipients,
            "subject": subject,
            "text": message,
        }

        # Add an HTML version when provided.
        if html_message:
            data["html"] = html_message

        # Add attachments when provided.
        if attachments:
            data["attachment"] = [
                (filename, content)
                for filename, content, _ in attachments
            ]

        # Send the email through the Mailgun API.
        response = self.client.messages.create(
            domain=settings.MAILGUN_DOMAIN,
            data=data,
        )

        # Mailgun returns a successful response when the message is queued.
        if response.status_code != 200:
            raise RuntimeError(
                f"Mailgun email failed with status {response.status_code}."
            )

        return 1