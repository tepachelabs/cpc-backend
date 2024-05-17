import logging
from typing import Optional

from cpc.app.models import CollectionReminder
from cpc.app.services.telegram import telegram_service
from cpc.shopify_backend.client import ShopifyClient

logger = logging.getLogger()


class ShopifyProductCountService:
    shopify_client = ShopifyClient()
    telegram_service = telegram_service

    def count_message(self, reminders: list[CollectionReminder]) -> Optional[str]:
        telegram_message = None
        messages = []
        for collection_reminder in reminders:
            collection = self.shopify_client.find_collection(
                shopify_id=collection_reminder.shopify_id
            )
            if collection is not None:
                logger.info(
                    f"CollectionReminder {collection_reminder.shopify_id} found, fetching products."
                )
                if not hasattr(collection, "products"):
                    continue
                products = collection.products()
                for product in products:
                    message = f"🏷️ *{product.title}*:\n"
                    if len(product.variants) == 1:
                        quantity = product.variants[0].inventory_quantity
                        message += f"> {self.telegram_service.parse_text(str(quantity))} \\-\\-\\-\\> {product.title}\n"
                        messages.append(message)
                    else:
                        for variant in product.variants:
                            quantity = variant.inventory_quantity
                            message += f"> {self.telegram_service.parse_text(str(quantity))} \\-\\-\\-\\> {variant.title}\n"
                        messages.append(message)
            else:
                logger.error(
                    f"CollectionReminder {collection_reminder.shopify_id} not found in Shopify."
                )

        if len(messages) > 0:
            telegram_message = "✨🚨 *Conteo de productos* 🚨✨\n\n"
            telegram_message += "\n\n".join(messages)
            telegram_message += "\n\n*"
            telegram_message += telegram_service.parse_text(
                f"Confirmar existencia con un mensaje 👍🏽"
            )
            telegram_message += "*\n\n*"
            telegram_message += telegram_service.parse_text(
                "Si hay discrepancia: hay que dar una razón."
            )
            telegram_message += "*"

        return telegram_message
