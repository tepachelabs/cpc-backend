import logging
from typing import Optional

from cpc.app.models import ProductReminder
from cpc.app.services.telegram import TelegramService
from cpc.shopify_backend.client import ShopifyClient

logger = logging.getLogger()


class ShopifyProductCountService:
    shopify_client = ShopifyClient().instance()

    def count_message(
        self, telegram: TelegramService, reminders: list[ProductReminder]
    ) -> Optional[str]:
        telegram_message = None
        messages = []
        for product_reminder in reminders:
            if (
                product_reminder.shopify_id is not None
                and product_reminder.shopify_id != ""
            ):
                product = self.shopify_client.find_product(
                    id=product_reminder.shopify_id
                )
            else:
                product = self.shopify_client.find_product(title=product_reminder.title)
            if product is not None:
                message = f"🏷️ *{product.title}*:\n"
                if len(product.variants) == 1:
                    quantity = product.variants[0].inventory_quantity
                    message += f"> {telegram.parse_text(str(quantity))} \\-\\-\\-\\> {product.title}\n"
                    messages.append(message)
                else:
                    for variant in product.variants:
                        quantity = variant.inventory_quantity
                        message += f"> {telegram.parse_text(str(quantity))} \\-\\-\\-\\> {variant.title}\n"
                    messages.append(message)
            else:
                logger.error(
                    f"ProductReminder {product_reminder.id} not found in Shopify."
                )

        if len(messages) > 0:
            telegram_message = "✨🚨 *Conteo de productos* 🚨✨\n\n"
            telegram_message += "\n\n".join(messages)
            telegram_message += (
                "\n\n *Confirmar existencia con una reaccion ó mensaje👍🏽*"
            )

        return telegram_message
