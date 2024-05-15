from __future__ import absolute_import, unicode_literals

import os

import logtail
from celery import Celery
from celery.schedules import crontab
from celery.signals import after_setup_logger

from cpc.settings import REDIS_URL, LOGTAIL_SOURCE_TOKEN

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cpc.settings")

app = Celery("cpc", broker=REDIS_URL, backend=REDIS_URL)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "close-reminder": {
        "task": "cpc.shopify_backend.tasks.inventory_reminder",
        "schedule": crontab(hour="4", minute="00"),  # Run at 9:00 PM Phoenix TZ
    },
    "open-reminder": {
        "task": "cpc.shopify_backend.tasks.inventory_reminder",
        "schedule": crontab(hour="13", minute="30"),  # Run at 6:30 AM Phoenix TZ
    },
    "notify-calendar-events": {
        "task": "cpc.app.tasks.notify_calendar_events",
        "schedule": crontab(hour="14", minute="00"),  # Run at 7:00 AM Phoenix TZ
    },
    # TODO: Uncomment when the webhook is ready
    # "register-calendar-webhook": {
    #     "task": "cpc.webhooks.tasks.register_calendar_webhook",
    #     "schedule": crontab(hour="7", minute="01"),  # Run at 0:01 AM Phoenix TZ
    # },
}


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    if LOGTAIL_SOURCE_TOKEN:
        handler = logtail.LogtailHandler(source_token=LOGTAIL_SOURCE_TOKEN)
        logger.addHandler(handler)
        logger.propagate = False
