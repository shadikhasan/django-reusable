# Django Reusable Template

A collection of reusable, modular components and integrations for Django projects.

The goal of this repository is to build common functionality once and reuse it across multiple Django projects without rebuilding the same features from scratch.

## Goals

- Build reusable Django components.
- Keep each component independent.
- Support multiple third-party providers where applicable.
- Follow standard Python and Django practices.
- Keep application code independent from external services.
- Make components easy to copy into new projects.
- Avoid unnecessary abstraction and over-engineering.

## Repository Structure

```text
django-reusable/
│
├── email/
│   ├── providers/
│   │   ├── base.py
│   │   ├── smtp.py
│   │   ├── resend.py
│   │   ├── sendgrid.py
│   │   ├── mailgun.py
│   │   ├── ses.py
│   │   ├── postmark.py
│   │   └── brevo.py
│   │
│   ├── templates/
│   ├── tests/
│   │   ├── test_service.py
│   │   └── test_providers/
│   │
│   ├── service.py
│   └── README.md
│
├── storage/
├── payment/
├── notification/
├── authentication/
├── logging/
│
└── README.md
````

## Components

### Email

Reusable email functionality with support for multiple providers.

Supported providers:

* SMTP
* Resend
* SendGrid
* Mailgun
* Amazon SES
* Postmark
* Brevo

See `email/README.md` for configuration and usage.

### Storage

Reusable file and object storage integrations.

Possible providers:

* Local storage
* Amazon S3
* Cloudinary
* Other object storage providers

### Payment

Reusable payment integrations.

Possible providers:

* Stripe
* PayPal
* Other payment providers

### Notification

Reusable notification functionality.

Possible channels:

* Email
* In-app notifications
* WebSocket
* Push notifications
* SMS

### Authentication

Reusable authentication functionality.

Possible features:

* JWT authentication
* Session authentication
* Email verification
* Password reset
* Social authentication
* OTP

### Logging

Reusable application logging and observability functionality.

Possible features:

* Structured logging
* Request logging
* Error logging
* Audit logging
* External logging integrations

## Design Principles

### 1. Modular

Each component should be independently reusable.

For example:

```text
email/
storage/
payment/
```

A project should be able to use one component without requiring unrelated components.

### 2. Provider Independent

When a component supports multiple providers, application code should interact with a common interface.

Example:

```python
EmailService().send(...)
```

The application does not need to know whether the email is being sent through SMTP, Resend, SendGrid, or another provider.

### 3. Simple

Prefer simple and well-known Python and Django patterns.

Avoid adding abstractions unless they provide a clear benefit.

### 4. Configuration Driven

Provider selection and credentials should be configured through Django settings and environment variables.

Example:

```python
EMAIL_PROVIDER = "resend"
```

Credentials should never be hard-coded.

### 5. Testable

Each component should contain its own tests.

External services should normally be mocked during unit tests.

### 6. Reusable

Components should be designed so they can be copied into another Django project with minimal modification.

## General Component Structure

A component should generally follow this structure:

```text
component/
├── providers/
│   ├── base.py
│   └── provider.py
│
├── templates/
├── tests/
├── service.py
└── README.md
```

Not every component needs every directory.

Only add files and directories that are actually required.

## Provider Architecture

Components that support multiple external providers use a common provider interface.

```text
                 Service
                    │
                    ▼
             Provider Interface
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
      Provider A Provider B Provider C
```

This keeps provider-specific implementation isolated from application code.

## Service Layer

The service layer provides the main entry point for application code.

Example:

```python
from email.service import EmailService

EmailService().send(
    subject="Welcome",
    to="user@example.com",
    message="Welcome!",
)
```

Application code should generally interact with the service instead of directly using provider SDKs.

## Configuration

Configuration belongs in Django settings.

Sensitive credentials should come from environment variables.

Example:

```python
EMAIL_PROVIDER = "resend"
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
```

Environment variables:

```env
DEFAULT_FROM_EMAIL=noreply@example.com
RESEND_API_KEY=re_xxxxxxxxx
```

Provider-specific configuration should only be added when that provider is used.

## Dependencies

Components should document their external dependencies.

For provider-based components, install only the SDKs required by the project.

For example:

```bash
pip install resend
```

Avoid making unrelated provider SDKs mandatory dependencies.

## Testing

Run tests for an individual component:

```bash
python manage.py test email
```

Run the complete test suite:

```bash
python manage.py test
```

External APIs should not normally be called during unit tests.

Use mocks or local test implementations instead.

## Adding a New Provider

When adding a provider:

1. Add the provider implementation.
2. Follow the common provider interface.
3. Register the provider with the service.
4. Add provider-specific tests.
5. Add required settings.
6. Add required environment variables.
7. Update the component README.
8. Document the required SDK.

## Adding a New Component

When adding a new component:

1. Create a dedicated directory.
2. Keep the component independent.
3. Define a common interface if multiple providers are supported.
4. Add a service layer when appropriate.
5. Add tests.
6. Add configuration documentation.
7. Add a component-level README.
8. Update the root README.

## Code Style

Follow standard Python and Django conventions.

Prefer:

* Clear names
* Type hints
* Class and function docstrings
* Small focused classes
* Simple control flow
* Explicit dependencies
* Consistent formatting

Avoid:

* Unnecessary abstractions
* Deep inheritance hierarchies
* Hard-coded credentials
* Provider-specific logic scattered throughout the application
* Unnecessary dependencies

## Reuse Workflow

When starting a new Django project:

```text
1. Select required components
        ↓
2. Copy the required components
        ↓
3. Install required dependencies
        ↓
4. Configure Django settings
        ↓
5. Configure environment variables
        ↓
6. Run tests
        ↓
7. Use the service layer
```

For example, if a project only needs email through Resend:

```text
email/
├── providers/
│   ├── base.py
│   └── resend.py
├── tests/
├── service.py
└── README.md
```

Install:

```bash
pip install resend
```

Configure:

```python
EMAIL_PROVIDER = "resend"
```

Then:

```python
EmailService().send(...)
```

## Contributing

Contributions are welcome.

When contributing:

* Keep changes focused.
* Follow the existing project structure.
* Follow Python and Django conventions.
* Add tests for new functionality.
* Update relevant documentation.
* Avoid unnecessary dependencies and abstractions.

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

## Disclaimer

This repository provides reusable implementation examples and integrations.

Third-party services, SDKs, trademarks, and APIs belong to their respective owners. Check their official documentation and licensing terms before using them in production.

