````markdown
# **Django Payments Module**

A reusable payment module for Django projects with support for multiple payment providers through a common interface.

## **Features**

- Common payment provider interface.
- Multiple provider support.
- Stripe support.
- PayPal support.
- Payment creation.
- Payment retrieval.
- Payment capture.
- Payment refunds.
- Webhook verification and handling.
- Provider selection through Django settings.
- Provider-specific implementations are isolated.

## **Structure**

```text
payments/

├── providers/
│   ├── base.py
│   ├── stripe.py
│   └── paypal.py
│
├── webhooks/
│   ├── base.py
│   ├── stripe.py
│   └── paypal.py
│
├── tests/
│   ├── test_service.py
│   ├── test_webhooks.py
│   └── test_providers/
│       ├── test_stripe.py
│       └── test_paypal.py
│
├── service.py
└── README.md
````

## **Architecture**

The module uses a common provider interface and a service layer.

```text
Application

     │

     ▼

PaymentService

     │

     ▼

PaymentProvider

     │

     ├── StripeProvider
     │
     └── PayPalProvider
```

The application only interacts with `PaymentService`.

The selected provider is controlled through Django settings.

## **Installation**

Install only the provider package you need.

### **Stripe**

```bash
pip install stripe
```

### **PayPal**

```bash
pip install paypal-checkout-serversdk
```

## **Configuration**

Set the provider in Django settings.

### **Stripe**

```python
PAYMENT_PROVIDER = "stripe"

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
```

### **PayPal**

```python
PAYMENT_PROVIDER = "paypal"

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")

PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")

PAYPAL_ENVIRONMENT = "sandbox"

PAYPAL_WEBHOOK_ID = os.getenv("PAYPAL_WEBHOOK_ID")
```

## **Environment Variables**

Keep credentials in environment variables.

Example:

```env
STRIPE_SECRET_KEY=sk_test_xxxxxxxxx

STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxx

PAYPAL_CLIENT_ID=xxxxxxxxx

PAYPAL_CLIENT_SECRET=xxxxxxxxx

PAYPAL_WEBHOOK_ID=xxxxxxxxx
```

Only configure the variables required by the selected provider.

## **Usage**

Import `PaymentService`:

```python
from payments.service import PaymentService
```

Create a payment:

```python
payment = PaymentService().create(
    amount=1000,
    currency="USD",
)
```

## **Retrieve Payment**

```python
PaymentService().get(
    payment_id="payment-id",
)
```

## **Capture Payment**

```python
PaymentService().capture(
    payment_id="payment-id",
)
```

## **Refund Payment**

```python
PaymentService().refund(
    payment_id="payment-id",
    amount=500,
    currency="USD",
)
```

For a full refund, omit `amount`.

```python
PaymentService().refund(
    payment_id="payment-id",
)
```

## **Changing Provider**

The application code does not need to change when switching providers.

For example:

```python
PAYMENT_PROVIDER = "stripe"
```

can be changed to:

```python
PAYMENT_PROVIDER = "paypal"
```

The application continues to use:

```python
PaymentService().create(...)
```

## **Webhooks**

Webhook handlers verify provider signatures before processing events.

### **Stripe**

```python
from payments.webhooks.stripe import StripeWebhookHandler

handler = StripeWebhookHandler()

event = handler.verify(
    request.body,
    dict(request.headers),
)

result = handler.handle(event)
```

### **PayPal**

```python
from payments.webhooks.paypal import PayPalWebhookHandler

handler = PayPalWebhookHandler()

event = handler.verify(
    request.body,
    dict(request.headers),
)

result = handler.handle(event)
```

## **Testing**

The test suite mocks external payment provider APIs.

Run all tests:

```bash
python manage.py test payments
```

Run service tests:

```bash
python manage.py test payments.tests.test_service
```

Run provider tests:

```bash
python manage.py test payments.tests.test_providers
```

Run webhook tests:

```bash
python manage.py test payments.tests.test_webhooks
```

External payment APIs are not called during unit tests.

## **Adding a New Provider**

Create a new provider inside:

```text
payments/providers/
```

Example:

```text
payments/providers/example.py
```

Implement `PaymentProvider`:

```python
from typing import Any

from .base import PaymentProvider


class ExampleProvider(PaymentProvider):
    """Payment provider using the Example API."""

    def create_payment(
        self,
        amount: int,
        currency: str,
        **kwargs: Any,
    ) -> Any:
        """
        Create a payment through the Example provider.

        Args:
            amount: Payment amount in the smallest currency unit.
            currency: Three-letter ISO 4217 currency code.
            **kwargs: Provider-specific options.

        Returns:
            Provider-specific payment information.
        """
        ...

    def get_payment(
        self,
        payment_id: str,
    ) -> Any:
        """
        Retrieve a payment from the Example provider.

        Args:
            payment_id: Provider payment identifier.

        Returns:
            Provider-specific payment information.
        """
        ...

    def capture_payment(
        self,
        payment_id: str,
        **kwargs: Any,
    ) -> Any:
        """
        Capture an authorized payment.

        Args:
            payment_id: Provider payment identifier.
            **kwargs: Provider-specific options.

        Returns:
            Provider-specific payment information.
        """
        ...

    def refund_payment(
        self,
        payment_id: str,
        amount: int | None = None,
        currency: str | None = None,
        **kwargs: Any,
    ) -> Any:
        """
        Refund a payment.

        Args:
            payment_id: Provider payment identifier.
            amount: Optional refund amount in the smallest currency unit.
            currency: Three-letter ISO 4217 currency code.
            **kwargs: Provider-specific options.

        Returns:
            Provider-specific refund information.
        """
        ...
```

Then register the provider in `service.py`:

```python
from .providers.example import ExampleProvider
```

```python
PROVIDERS: dict[str, type[PaymentProvider]] = {
    "stripe": StripeProvider,
    "paypal": PayPalProvider,
    "example": ExampleProvider,
}
```

Then configure:

```python
PAYMENT_PROVIDER = "example"
```

## **Design Principles**

* Keep provider implementations isolated.

* Keep application code independent of payment providers.

* Use one common provider interface.

* Keep provider credentials in Django settings/environment variables.

* Avoid provider-specific code in application services.

* Keep the module reusable across Django projects.

* Add only the provider dependencies required by each project.

## **License**

Use according to the license of the parent project.

