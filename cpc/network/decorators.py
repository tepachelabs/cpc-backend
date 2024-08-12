import json
import logging
from functools import wraps

from django.conf import settings

logger = logging.getLogger(__name__)


def log_raw_json(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        if settings.DEBUG:
            raw_body = request.body
            try:
                parsed_body = json.loads(raw_body)
                pretty_body = json.dumps(parsed_body, indent=4)
                logger.info(f"Raw request body:\n{pretty_body}\n\n")
            except json.JSONDecodeError:
                logger.warning("Failed to decode JSON from request body")
        return func(self, request, *args, **kwargs)

    return wrapper
