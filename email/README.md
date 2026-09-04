````markdown
# Django Email Module

A reusable email module for Django projects with support for multiple email providers through a common interface.

## Features

- Common email provider interface.
- Multiple provider support.
- SMTP support through Django's email backend.
- Resend support.
- SendGrid support.
- Mailgun support.
- Amazon SES support.
- Postmark support.
- Brevo support.
- Plain-text emails.
- HTML emails.
- Email attachments.
- Configurable default sender.
- Provider selection through Django settings.
- Provider-specific implementations are isolated.

## Structure

```text
email/
├── providers/
│   ├── base.py
│   ├── smtp.py
│   ├── resend.py
│   ├── sendgrid.py
│   ├── mailgun.py
│   ├── ses.py
│   ├── postmark.py
│   └── brevo.py
│
├── templates/
├── tests/
│   ├── test_service.py
│   └── test_providers/
│       ├── test_smtp.py
│       ├── test_resend.py
│       ├── test_sendgrid.py
│       ├── test_mailgun.py
│       ├── test_ses.py
│       ├── test_postmark.py
│       └── test_brevo.py
│
├── service.py
└── README.md
````

## Architecture

The module uses a common provider interface and a service layer.

```text
Application
     │
     ▼
EmailService
     │
     ▼
EmailProvider
     │
     ├── SMTPProvider
     ├── ResendProvider
     ├── SendGridProvider
     ├── MailgunProvider
     ├── SESProvider
     ├── PostmarkProvider
     └── BrevoProvider
```

The application only interacts with `EmailService`.

The selected provider is controlled through Django settings.

## Installation

Install only the provider package you need.

### SMTP

No additional package is required.

### Resend

```bash
pip install resend
```

### SendGrid

```bash
pip install sendgrid
```

### Mailgun

```bash
pip install mailgun-python
```

### Amazon SES

```bash
pip install boto3
```

### Postmark

```bash
pip install postmark-python
```

### Brevo

```bash
pip install brevo-python
```

## Configuration

Set the provider in Django settings.

### SMTP

```python
EMAIL_PROVIDER = "smtp"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
```

### Resend

```python
EMAIL_PROVIDER = "resend"

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
```

### SendGrid

```python
EMAIL_PROVIDER = "sendgrid"

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
```

### Mailgun

```python
EMAIL_PROVIDER = "mailgun"

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
```

### Amazon SES

```python
EMAIL_PROVIDER = "ses"

AWS_SES_REGION = os.getenv("AWS_SES_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
```

### Postmark

```python
EMAIL_PROVIDER = "postmark"

POSTMARK_SERVER_TOKEN = os.getenv("POSTMARK_SERVER_TOKEN")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
```

### Brevo

```python
EMAIL_PROVIDER = "brevo"

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
```

## Environment Variables

Keep credentials in environment variables.

Example:

```env
DEFAULT_FROM_EMAIL=noreply@example.com

EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=username
EMAIL_HOST_PASSWORD=password

RESEND_API_KEY=re_xxxxxxxxx

SENDGRID_API_KEY=SG.xxxxxxxxx

MAILGUN_API_KEY=key-xxxxxxxxx
MAILGUN_DOMAIN=mg.example.com

AWS_SES_REGION=us-east-1
AWS_ACCESS_KEY_ID=xxxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxxx

POSTMARK_SERVER_TOKEN=xxxxxxxxx

BREVO_API_KEY=xxxxxxxxx
```

Only configure the variables required by the selected provider.

## Usage

Import `EmailService`:

```python
from email.service import EmailService
```

Send a basic email:

```python
EmailService().send(
    subject="Welcome",
    to="user@example.com",
    message="Welcome to our application!",
)
```

## Multiple Recipients

```python
EmailService().send(
    subject="Announcement",
    to=[
        "user1@example.com",
        "user2@example.com",
    ],
    message="This is an announcement.",
)
```

## HTML Email

```python
EmailService().send(
    subject="Welcome",
    to="user@example.com",
    message="Welcome to our application!",
    html_message="<h1>Welcome!</h1><p>Thank you for joining us.</p>",
)
```

## Custom Sender

By default, the module uses:

```python
DEFAULT_FROM_EMAIL
```

A custom sender can be provided when required:

```python
EmailService().send(
    subject="Notification",
    to="user@example.com",
    message="Your notification.",
    from_email="notifications@example.com",
)
```

## Attachments

Attachments use Django-style tuples:

```python
attachments = [
    (
        "report.pdf",
        pdf_content,
        "application/pdf",
    ),
]
```

Then:

```python
EmailService().send(
    subject="Your Report",
    to="user@example.com",
    message="Please find your report attached.",
    attachments=attachments,
)
```

The expected attachment format is:

```text
(filename, content, mimetype)
```

## Changing Provider

The application code does not need to change when switching providers.

For example:

```python
EMAIL_PROVIDER = "resend"
```

can be changed to:

```python
EMAIL_PROVIDER = "sendgrid"
```

The application continues to use:

```python
EmailService().send(...)
```

## Testing

The test suite uses Django's local memory email backend for SMTP and mocks external provider APIs.

Run all tests:

```bash
python manage.py test email
```

Run only service tests:

```bash
python manage.py test email.tests.test_service
```

Run provider tests:

```bash
python manage.py test email.tests.test_providers
```

External email APIs are not called during unit tests.

## Adding a New Provider

Create a new provider inside:

```text
email/providers/
```

Example:

```text
email/providers/example.py
```

Implement `EmailProvider`:

```python
from typing import Sequence

from .base import EmailProvider


class ExampleProvider(EmailProvider):
    """Email provider using the Example API."""

    def __init__(self):
        """Initialize the Example client."""

    def send(
        self,
        subject: str,
        to: str | Sequence[str],
        message: str,
        html_message: str | None = None,
        from_email: str | None = None,
        attachments: Sequence[tuple] | None = None,
    ) -> int:
        """
        Send an email through the Example provider.

        Args:
            subject: Email subject.
            to: Recipient email address or a sequence of addresses.
            message: Plain-text email body.
            html_message: Optional HTML email body.
            from_email: Optional sender email address.
            attachments: Optional sequence of Django-style attachment tuples.

        Returns:
            Number of successfully sent messages.
        """
        ...
```

Then register the provider in `service.py`:

```python
from .providers.example import ExampleProvider
```

```python
PROVIDERS: dict[str, type[EmailProvider]] = {
    "smtp": SMTPProvider,
    "resend": ResendProvider,
    "sendgrid": SendGridProvider,
    "mailgun": MailgunProvider,
    "ses": SESProvider,
    "postmark": PostmarkProvider,
    "brevo": BrevoProvider,
    "example": ExampleProvider,
}
```

Then configure:

```python
EMAIL_PROVIDER = "example"
```

## Design Principles

* Keep provider implementations isolated.
* Keep application code independent of email providers.
* Use one common provider interface.
* Keep provider credentials in Django settings/environment variables.
* Avoid provider-specific code in application services.
* Keep the module reusable across Django projects.
* Add only the provider dependencies required by each project.

## License

Use according to the license of the parent project.

```

This README is suitable as the **final documentation for the reusable email module**.
```
