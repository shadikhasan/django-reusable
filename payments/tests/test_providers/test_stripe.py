from unittest.mock import patch

from payments.providers.stripe import StripeProvider


@patch("payments.providers.stripe.stripe.PaymentIntent.create")
def test_create_payment(mock_create):
    mock_create.return_value = {"id": "pi_123"}

    provider = StripeProvider()

    result = provider.create_payment(1000, "USD")

    assert result == {"id": "pi_123"}
    mock_create.assert_called_once_with(
        amount=1000,
        currency="USD",
    )


@patch("payments.providers.stripe.stripe.PaymentIntent.retrieve")
def test_get_payment(mock_retrieve):
    mock_retrieve.return_value = {"id": "pi_123"}

    provider = StripeProvider()

    result = provider.get_payment("pi_123")

    assert result == {"id": "pi_123"}
    mock_retrieve.assert_called_once_with("pi_123")


@patch("payments.providers.stripe.stripe.PaymentIntent.capture")
def test_capture_payment(mock_capture):
    mock_capture.return_value = {"id": "pi_123"}

    provider = StripeProvider()

    result = provider.capture_payment("pi_123")

    assert result == {"id": "pi_123"}
    mock_capture.assert_called_once_with("pi_123")


@patch("payments.providers.stripe.stripe.Refund.create")
def test_refund_payment(mock_refund):
    mock_refund.return_value = {"id": "re_123"}

    provider = StripeProvider()

    result = provider.refund_payment(
        "pi_123",
        amount=500,
        currency="USD",
    )

    assert result == {"id": "re_123"}
    mock_refund.assert_called_once_with(
        payment_intent="pi_123",
        amount=500,
    )