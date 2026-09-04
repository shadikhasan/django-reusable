from unittest.mock import patch

from django.test import SimpleTestCase, override_settings

from email.providers.brevo import BrevoProvider


@override_settings(
    DEFAULT_FROM_EMAIL="noreply@example.com",
    BREVO_API_KEY="test-api-key",
)
class BrevoProviderTest(SimpleTestCase):
    """Test the Brevo email provider."""

    @patch("email.providers.brevo.Brevo")
    def test_send_email(self, mock_client):
        """Test sending an email through Brevo."""
        result = BrevoProvider().send(
            subject="Test Email",
            to="user@example.com",
            message="Hello!",
        )

        self.assertEqual(result, 1)
        mock_client.return_value.transactional_emails.send_transac_email.assert_called_once()