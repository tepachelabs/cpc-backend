import asyncio
import logging

from celery import shared_task

from cpc import settings
from cpc.app.models import ProductReminder
from cpc.app.services.telegram import TelegramService
from cpc.shopify_backend.services import ShopifyProductCountService

logger = logging.getLogger()


@shared_task
def inventory_reminder():
    reminders = ProductReminder.objects.all()
    if reminders.count() == 0:
        logger.info("No reminders found.")
        return

    telegram = TelegramService(settings.TELEGRAM_BOT_TOKEN)

    telegram_message = ShopifyProductCountService().count_message(telegram, reminders)

    if telegram_message is None:
        logger.info("No message generated.")
        return

    # Make the async call sync at this point only.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(telegram.send_message(telegram_message))
    finally:
        loop.close()
