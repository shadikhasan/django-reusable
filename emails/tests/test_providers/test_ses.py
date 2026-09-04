from unittest.mock import patch

from django.test import SimpleTestCase, override_settings

from email.providers.ses import SESProvider


@override_settings(
    DEFAULT_FROM_EMAIL="noreply@example.com",
    AWS_SES_REGION="us-east-1",
    AWS_ACCESS_KEY_ID="test-access-key",
    AWS_SECRET_ACCESS_KEY="test-secret-key",
)
class SESProviderTest(SimpleTestCase):
    """Test the Amazon SES email provider."""

    @patch("email.providers.ses.boto3.client")
    def test_send_email(self, mock_client):
        """Test sending an email through Amazon SES."""
        result = SESProvider().send(
            subject="Test Email",
            to="user@example.com",
            message="Hello!",
        )

        self.assertEqual(result, 1)
        mock_client.return_value.send_email.assert_called_once()