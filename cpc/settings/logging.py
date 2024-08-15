import os

from ._base import PRODUCTION
from ..logging import IgnorePatternFilter

LOGTAIL_SOURCE_TOKEN = os.getenv("LOGTAIL_SOURCE_TOKEN", None)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "ignore_pattern_telegram_http_filter": {
            "()": IgnorePatternFilter,
            "pattern": r"HTTP Request.+https://api\.telegram\.org/bot(\d+:[\w-]+).+",
        },
    },
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
            "propagate": False,
        },
        "httpx": {
            "level": "INFO",
            "filters": ["ignore_pattern_telegram_http_filter"],
            "propagate": False,
        },
    },
}

if PRODUCTION and LOGTAIL_SOURCE_TOKEN is not None:
    LOGGING["root"]["handlers"].append("logtail")
