from unittest.mock import Mock, patch

from payments.service import PaymentService


def get_service():
    provider = Mock()

    with patch(
        "payments.service.PROVIDERS",
        {"test": lambda: provider},
    ):
        with patch(
            "payments.service.settings.PAYMENT_PROVIDER",
            "test",
        ):
            service = PaymentService()

    return service, provider


def test_create():
    service, provider = get_service()

    provider.create_payment.return_value = {"id": "pay_123"}

    result = service.create(1000, "USD")

    assert result == {"id": "pay_123"}


def test_get():
    service, provider = get_service()

    provider.get_payment.return_value = {"id": "pay_123"}

    result = service.get("pay_123")

    assert result == {"id": "pay_123"}


def test_capture():
    service, provider = get_service()

    provider.capture_payment.return_value = {"id": "pay_123"}

    result = service.capture("pay_123")

    assert result == {"id": "pay_123"}


def test_refund():
    service, provider = get_service()

    provider.refund_payment.return_value = {"id": "refund_123"}

    result = service.refund("pay_123", 500, "USD")

    assert result == {"id": "refund_123"}