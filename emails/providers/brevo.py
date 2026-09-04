from typing import Sequence

from brevo import Brevo
from brevo.transactional_emails import (
    SendTransacEmailRequestSender,
    SendTransacEmailRequestToItem,
)
from django.conf import settings

from .base import EmailProvider


class BrevoProvider(EmailProvider):
    """Email provider using the Brevo API."""

    def __init__(self):
        """Initialize the Brevo client with the configured API key."""
        self.client = Brevo(api_key=settings.BREVO_API_KEY)

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
        Send an email through Brevo.

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

        # Build the recipient list for the Brevo API.
        recipient_list = [
            SendTransacEmailRequestToItem(email=recipient)
            for recipient in recipients
        ]

        # Build the sender information for the Brevo API.
        sender_data = SendTransacEmailRequestSender(email=sender)

        # Build the email payload with the required fields.
        params = {
            "sender": sender_data,
            "to": recipient_list,
            "subject": subject,
        }

        # Use HTML content when provided; otherwise use plain text.
        if html_message:
            params["html_content"] = html_message
        else:
            params["text_content"] = message

        # Add attachments when provided.
        if attachments:
            params["attachment"] = [
                {
                    "name": filename,
                    "content": content,
                }
                for filename, content, _ in attachments
            ]

        # Send the email through the Brevo API.
        self.client.transactional_emails.send_transac_email(**params)

        return 1