import sentry_sdk
import os
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_dsn = os.getenv('SENTRY_DSN', None)

if sentry_dsn is not None and len(sentry_dsn) > 0:
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[
            FlaskIntegration(),
        ],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )
