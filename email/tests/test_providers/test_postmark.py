from unittest.mock import patch

from django.test import SimpleTestCase, override_settings

from email.providers.postmark import PostmarkProvider


@override_settings(
    DEFAULT_FROM_EMAIL="noreply@example.com",
    POSTMARK_SERVER_TOKEN="test-server-token",
)
class PostmarkProviderTest(SimpleTestCase):
    """Test the Postmark email provider."""

    @patch("email.providers.postmark.postmark.sync.ServerClient")
    def test_send_email(self, mock_client):
        """Test sending an email through Postmark."""
        result = PostmarkProvider().send(
            subject="Test Email",
            to="user@example.com",
            message="Hello!",
        )

        self.assertEqual(result, 1)
        mock_client.return_value.outbound.send.assert_called_once()