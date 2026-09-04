from unittest.mock import patch

from django.test import SimpleTestCase, override_settings

from email.providers.resend import ResendProvider


@override_settings(
    DEFAULT_FROM_EMAIL="noreply@example.com",
    RESEND_API_KEY="test-api-key",
)
class ResendProviderTest(SimpleTestCase):
    """Test the Resend email provider."""

    @patch("email.providers.resend.resend.Emails.send")
    def test_send_email(self, mock_send):
        """Test sending an email through Resend."""
        result = ResendProvider().send(
            subject="Test Email",
            to="user@example.com",
            message="Hello!",
        )

        self.assertEqual(result, 1)
        mock_send.assert_called_once()