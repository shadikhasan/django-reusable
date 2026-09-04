from typing import Sequence

from django.conf import settings

from .providers.base import EmailProvider
from .providers.brevo import BrevoProvider
from .providers.mailgun import MailgunProvider
from .providers.postmark import PostmarkProvider
from .providers.resend import ResendProvider
from .providers.sendgrid import SendGridProvider
from .providers.ses import SESProvider
from .providers.smtp import SMTPProvider


# Available email providers.
PROVIDERS: dict[str, type[EmailProvider]] = {
    "smtp": SMTPProvider,
    "resend": ResendProvider,
    "sendgrid": SendGridProvider,
    "mailgun": MailgunProvider,
    "ses": SESProvider,
    "postmark": PostmarkProvider,
    "brevo": BrevoProvider,
}

class EmailService:
    """High-level service for sending emails."""

    def __init__(self):
        # Select the provider configured in Django settings.
        provider_class = PROVIDERS.get(settings.EMAIL_PROVIDER)

        if provider_class is None:
            raise ValueError(
                f"Unsupported email provider: {settings.EMAIL_PROVIDER}"
            )

        self.provider = provider_class()

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
        Send an email using the configured email provider.

        Args:
            subject: Email subject.
            to: Recipient email address or addresses.
            message: Plain-text email body.
            html_message: Optional HTML email body.
            from_email: Optional sender email address.
            attachments: Optional email attachments.

        Returns:
            Number of successfully sent messages.
        """
        return self.provider.send(
            subject=subject,
            to=to,
            message=message,
            html_message=html_message,
            from_email=from_email,
            attachments=attachments,
        )