from typing import Sequence

import resend
from django.conf import settings

from .base import EmailProvider


class ResendProvider(EmailProvider):
    """Email provider using the Resend API."""

    def __init__(self):
        """Initialize Resend with the configured API key."""
        resend.api_key = settings.RESEND_API_KEY

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
        Send an email through Resend.

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

        # Build the email payload with the required fields.
        params: resend.Emails.SendParams = {
            "from": from_email or settings.DEFAULT_FROM_EMAIL,
            "to": recipients,
            "subject": subject,
            "text": message,
        }

        # Add an HTML version when provided.
        if html_message:
            params["html"] = html_message

        # Add attachments when provided.
        if attachments:
            params["attachments"] = [
                {
                    "filename": filename,
                    "content": content,
                }
                for filename, content, _ in attachments
            ]

        # Send the email through the Resend API.
        resend.Emails.send(params)

        return 1