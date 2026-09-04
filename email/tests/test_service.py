from django.core import mail
from django.test import SimpleTestCase, override_settings

from email.service import EmailService


@override_settings(
    EMAIL_PROVIDER="smtp",
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="noreply@example.com",
)
class EmailServiceTest(SimpleTestCase):
    """Test the email service."""

    def test_send_email(self):
        """Test sending an email through the configured provider."""
        result = EmailService().send(
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

    @override_settings(EMAIL_PROVIDER="invalid")
    def test_unsupported_provider(self):
        """Test that an unsupported provider raises an error."""
        with self.assertRaises(ValueError):
            EmailService()