from django.core import mail
from django.test import SimpleTestCase, override_settings

from email.providers.smtp import SMTPProvider


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="noreply@example.com",
)
class SMTPProviderTest(SimpleTestCase):
    """Test the SMTP email provider."""

    def test_send_email(self):
        """Test sending an email through SMTP."""
        result = SMTPProvider().send(
            subject="Test Email",
            to="user@example.com",
            message="Hello!",
        )

        self.assertEqual(result, 1)
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]

        self.assertEqual(email.subject, "Test Email")
        self.assertEqual(email.to, ["user@example.com"])
        self.assertEqual(email.body, "Hello!")