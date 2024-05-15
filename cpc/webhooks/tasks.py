import logging

from celery import shared_task

from cpc.webhooks.services.google.calendar import RegisterGoogleCalendarWebhookService

logger = logging.getLogger()


@shared_task
def register_calendar_webhook():
    try:
        RegisterGoogleCalendarWebhookService().call()
    except Exception as e:
        logger.error(f"Error registering Google Calendar webhook.", exc_info=e)
