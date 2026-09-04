from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase, override_settings

from email.providers.mailgun import MailgunProvider


@override_settings(
    DEFAULT_FROM_EMAIL="noreply@example.com",
    MAILGUN_API_KEY="test-api-key",
    MAILGUN_DOMAIN="example.com",
)
class MailgunProviderTest(SimpleTestCase):
    """Test the Mailgun email provider."""

    @patch("email.providers.mailgun.Client")
    def test_send_email(self, mock_client):
        """Test sending an email through Mailgun."""
        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_client.return_value.messages.create.return_value = mock_response

        result = MailgunProvider().send(
            subject="Test Email",
            to="user@example.com",
            message="Hello!",
        )

        self.assertEqual(result, 1)
        mock_client.return_value.messages.create.assert_called_once()