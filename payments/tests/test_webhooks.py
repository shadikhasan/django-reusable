import json
from unittest.mock import Mock, patch

from payments.webhooks.paypal import PayPalWebhookHandler
from payments.webhooks.stripe import StripeWebhookHandler


def test_stripe_handle():
    handler = StripeWebhookHandler()

    event = Mock()
    event.data.object = {"id": "pi_123"}

    result = handler.handle(event)

    assert result == {"id": "pi_123"}


@patch("payments.webhooks.stripe.stripe.Webhook.construct_event")
def test_stripe_verify(mock_construct):
    event = {"id": "evt_123"}
    mock_construct.return_value = event

    handler = StripeWebhookHandler()

    result = handler.verify(
        b'{"id":"evt_123"}',
        {"Stripe-Signature": "signature"},
    )

    assert result == event


def test_paypal_handle():
    handler = PayPalWebhookHandler()

    event = {"id": "WH-123"}

    result = handler.handle(event)

    assert result == event


@patch("payments.webhooks.paypal.requests.post")
def test_paypal_verify(mock_post):
    mock_post.return_value.json.return_value = {
        "verification_status": "SUCCESS"
    }
    mock_post.return_value.raise_for_status = Mock()

    handler = PayPalWebhookHandler()

    payload = json.dumps({"id": "WH-123"}).encode()

    headers = {
        "PAYPAL-AUTH-ALGO": "SHA256withRSA",
        "PAYPAL-CERT-URL": "https://example.com/cert",
        "PAYPAL-TRANSMISSION-ID": "transmission-123",
        "PAYPAL-TRANSMISSION-SIG": "signature",
        "PAYPAL-TRANSMISSION-TIME": "2026-09-05T10:00:00Z",
    }

    result = handler.verify(payload, headers)

    assert result == {"id": "WH-123"}