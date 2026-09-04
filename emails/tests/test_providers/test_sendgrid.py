from unittest.mock import patch

from django.test import SimpleTestCase, override_settings

from email.providers.sendgrid import SendGridProvider


@override_settings(
    DEFAULT_FROM_EMAIL="noreply@example.com",
    SENDGRID_API_KEY="test-api-key",
)
class SendGridProviderTest(SimpleTestCase):
    """Test the SendGrid email provider."""

    @patch("email.providers.sendgrid.SendGridAPIClient.send")
    def test_send_email(self, mock_send):
        """Test sending an email through SendGrid."""
        mock_send.return_value.status_code = 202

        result = SendGridProvider().send(
            subject="Test Email",
            to="user@example.com",
            message="Hello!",
        )

        self.assertEqual(result, 1)
        mock_send.assert_called_once()