from email.message import EmailMessage
from typing import Sequence

import boto3
from django.conf import settings

from .base import EmailProvider


class SESProvider(EmailProvider):
    """Email provider using the Amazon SES API."""

    def __init__(self):
        """Initialize the Amazon SES client with the configured credentials."""
        self.client = boto3.client(
            "sesv2",
            region_name=settings.AWS_SES_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

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
        Send an email through Amazon SES.

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

        # Build the MIME email so text, HTML, and attachments use one format.
        email = EmailMessage()
        email["Subject"] = subject
        email["From"] = sender
        email["To"] = ", ".join(recipients)
        email.set_content(message)

        # Add an HTML alternative when provided.
        if html_message:
            email.add_alternative(html_message, subtype="html")

        # Add attachments when provided.
        if attachments:
            for filename, content, mimetype in attachments:
                maintype, subtype = mimetype.split("/", 1)
                email.add_attachment(
                    content,
                    maintype=maintype,
                    subtype=subtype,
                    filename=filename,
                )

        # Send the MIME message through the SESv2 API.
        self.client.send_email(
            FromEmailAddress=sender,
            Destination={"ToAddresses": recipients},
            Content={
                "Raw": {
                    "Data": email.as_bytes(),
                }
            },
        )

        return 1