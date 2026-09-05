from unittest.mock import Mock, patch

from payments.providers.paypal import PayPalProvider


@patch("payments.providers.paypal.PayPalHttpClient")
def test_create_payment(mock_client):
    client = Mock()
    mock_client.return_value = client

    client.execute.return_value.result = {"id": "ORDER-123"}

    provider = PayPalProvider()

    result = provider.create_payment(1000, "USD")

    assert result == {"id": "ORDER-123"}
    client.execute.assert_called_once()


@patch("payments.providers.paypal.PayPalHttpClient")
def test_get_payment(mock_client):
    client = Mock()
    mock_client.return_value = client

    client.execute.return_value.result = {"id": "ORDER-123"}

    provider = PayPalProvider()

    result = provider.get_payment("ORDER-123")

    assert result == {"id": "ORDER-123"}
    client.execute.assert_called_once()


@patch("payments.providers.paypal.PayPalHttpClient")
def test_capture_payment(mock_client):
    client = Mock()
    mock_client.return_value = client

    client.execute.return_value.result = {"id": "ORDER-123"}

    provider = PayPalProvider()

    result = provider.capture_payment("ORDER-123")

    assert result == {"id": "ORDER-123"}
    client.execute.assert_called_once()


@patch("payments.providers.paypal.PayPalHttpClient")
def test_refund_payment(mock_client):
    client = Mock()
    mock_client.return_value = client

    client.execute.return_value.result = {"id": "REFUND-123"}

    provider = PayPalProvider()

    result = provider.refund_payment(
        "CAPTURE-123",
        amount=500,
        currency="USD",
    )

    assert result == {"id": "REFUND-123"}
    client.execute.assert_called_once()


def test_partial_refund_requires_currency():
    with patch("payments.providers.paypal.PayPalHttpClient"):
        provider = PayPalProvider()

        try:
            provider.refund_payment("CAPTURE-123", amount=500)
            assert False
        except ValueError:
            assert True