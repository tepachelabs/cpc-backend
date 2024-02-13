import logging

from celery import shared_task

from cpc import settings
from cpc.app.models import ProductReminder
from cpc.app.services.telegram import TelegramService
from cpc.shopify_backend.client import ShopifyClient

logger = logging.getLogger()


@shared_task
def inventory_reminder():
    reminders = ProductReminder.objects.all()
    if reminders.count() == 0:
        logger.info("No reminders found.")
        return

    telegram = TelegramService(settings.TELEGRAM_BOT_TOKEN)

    shopify_client = ShopifyClient().instance()
    messages = []
    for product_reminder in reminders:
        if (
            product_reminder.shopify_id is not None
            and product_reminder.shopify_id != ""
        ):
            product = shopify_client.find_product(id=product_reminder.shopify_id)
        else:
            product = shopify_client.find_product(title=product_reminder.title)
        if product is not None:
            if len(product.variants) == 1:
                messages.append(
                    f"> {telegram.parse_text(product.variants[0].inventory_quantity)} \\-\\-\\-\\> {product.title}"
                )
            else:
                message = f"🏷️ *{product.title}*:\n"
                for variant in product.variants:
                    message += f"> {telegram.parse_text(variant.inventory_quantity)} \\-\\-\\-\\> {variant.title}\n"
                messages.append(message)
        else:
            logger.error(f"ProductReminder {product_reminder.id} not found in Shopify.")

    if len(messages) > 0:
        telegram_message = "✨🚨 *Conteo de productos* 🚨✨\n\n"
        telegram_message += "\n\n".join(messages)
        telegram_message += "\n\n *Confirmar existencia con una reaccion ó mensaje👍🏽*"
        telegram.send_message(telegram_message)
