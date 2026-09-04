from typing import Sequence

from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Attachment,
    Content,
    FileContent,
    FileName,
    FileType,
    Mail,
)

from .base import EmailProvider


class SendGridProvider(EmailProvider):
    """Email provider using the SendGrid API."""

    def __init__(self):
        """Initialize the SendGrid client with the configured API key."""
        self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)

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
        Send an email through SendGrid.

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

        Raises:
            RuntimeError: If SendGrid does not accept the email.
        """
        recipients = [to] if isinstance(to, str) else list(to)
        sender = from_email or settings.DEFAULT_FROM_EMAIL

        # Create the email with the required plain-text content.
        mail = Mail(
            from_email=sender,
            to_emails=recipients,
            subject=subject,
            plain_text_content=Content("text/plain", message),
        )

        # Add an HTML alternative when provided.
        if html_message:
            mail.add_content(
                Content("text/html", html_message)
            )

        # Convert Django attachment tuples to SendGrid attachments.
        if attachments:
            for filename, content, mimetype in attachments:
                mail.add_attachment(
                    Attachment(
                        FileContent(content),
                        FileName(filename),
                        FileType(mimetype),
                    )
                )

        # Send the email through the SendGrid API.
        response = self.client.send(mail)

        if response.status_code not in (200, 202):
            raise RuntimeError(
                f"SendGrid email failed with status {response.status_code}."
            )

        return 1