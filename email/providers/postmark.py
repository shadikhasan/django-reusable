from typing import Sequence

import postmark.sync
from django.conf import settings

from .base import EmailProvider


class PostmarkProvider(EmailProvider):
    """Email provider using the Postmark API."""

    def __init__(self):
        """Initialize the Postmark client with the configured server token."""
        self.client = postmark.sync.ServerClient(settings.POSTMARK_SERVER_TOKEN)

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
        Send an email through Postmark.

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
            "sender": sender,
            "to": ", ".join(recipients),
            "subject": subject,
            "text_body": message,
        }

        # Add an HTML version when provided.
        if html_message:
            data["html_body"] = html_message

        # Add attachments when provided.
        if attachments:
            data["attachments"] = [
                {
                    "name": filename,
                    "content": content,
                    "content_type": mimetype,
                }
                for filename, content, mimetype in attachments
            ]

        # Send the email through the Postmark API.
        self.client.outbound.send(data)

        return 1