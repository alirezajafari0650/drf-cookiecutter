import sentry_sdk
from decouple import config

sentry_sdk.init(
    dsn=config("SENTRY_DSN"),
    integrations=[sentry_sdk.integrations.django.DjangoIntegration()],
    traces_sample_rate=1.0,  # performance monitoring (0.0–1.0)
    send_default_pii=True,  # optional – includes user info if logged in
)
