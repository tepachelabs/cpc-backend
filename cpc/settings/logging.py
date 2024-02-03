import os

from ._base import ENVIRONMENT

LOGTAIL_SOURCE_TOKEN = os.getenv("LOGTAIL_SOURCE_TOKEN", None)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "logtail": {
            "class": "logtail.LogtailHandler",
            "source_token": LOGTAIL_SOURCE_TOKEN,
        },
    },
    "root": {
        "handlers": [
            "console",
        ],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": [
                "console",
            ],
            "level": "INFO",
        },
    },
}

# if PRODUCTION and LOGTAIL_SOURCE_TOKEN is not None:
LOGGING["root"]["handlers"].append("logtail")
