import logging

from celery import shared_task

from cpc.app.models import CollectionReminder
from cpc.app.services.telegram import telegram_service
from cpc.shopify_backend.services import ShopifyProductCountService

logger = logging.getLogger()


@shared_task
def inventory_reminder():
    reminders = CollectionReminder.objects.all()
    if reminders.count() == 0:
        logger.info("No reminders found.")
        return

    service = ShopifyProductCountService()
    telegram_message = service.count_message(reminders)

    if telegram_message is None:
        logger.info("No message generated.")
        return

    telegram_service.send_message(telegram_message)
