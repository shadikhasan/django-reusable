from typing import Sequence

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail

from .base import EmailProvider


class SMTPProvider(EmailProvider):
    """
    Email provider using Django's SMTP email backend.

    Uses Django's high-level ``send_mail`` API for standard emails
    and ``EmailMultiAlternatives`` when attachments are required.
    """

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
        Send an email through the configured SMTP backend.

        For emails without attachments, Django's ``send_mail`` is used.
        When attachments are provided, ``EmailMultiAlternatives`` is used.

        Args:
            subject: Email subject.
            to: Recipient email address or a sequence of addresses.
            message: Plain-text email body.
            html_message: Optional HTML email body.
            from_email: Optional sender email address.
            attachments: Optional sequence of attachment tuples in the
                format ``(filename, content, mimetype)``.

        Returns:
            Number of messages successfully delivered.
        """
        recipients = [to] if isinstance(to, str) else list(to)
        sender = from_email or settings.DEFAULT_FROM_EMAIL

        if not attachments:
            return send_mail(
                subject=subject,
                message=message,
                from_email=sender,
                recipient_list=recipients,
                html_message=html_message,
            )

        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=sender,
            to=recipients,
        )

        if html_message:
            email.attach_alternative(
                html_message,
                "text/html",
            )

        for attachment in attachments:
            email.attach(*attachment)

        return email.send()