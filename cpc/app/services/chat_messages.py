import logging
from datetime import datetime

import pytz
from django.conf import settings

from cpc.app.services import GoogleCalendarService
from cpc.app.services.telegram import telegram_service, TelegramMessageParser
from cpc.shopify_backend.data import OrderCreateData

logger = logging.getLogger(__name__)


class NewOrderChatMessageService:
    telegram_service = telegram_service
    telegram_message_parser = TelegramMessageParser()

    def send_message(self, order_data: OrderCreateData):
        message = f"📦 *Nueva Orden Web Recibida*: {self.telegram_message_parser.call(str(order_data.order_number))}\n\n"
        message += (
            f"💰 *Total*: ${self.telegram_message_parser.call(order_data.total_price)}\n"
        )
        message += f"🔖 *Etiquetar para*: {self.telegram_message_parser.call(order_data.customer_name)}\n"
        message += "\n"
        message += "*Artículos en la Orden:*\n"
        for item in order_data.order_create_line_items:
            message += (
                f"{self.telegram_message_parser.call('-')}"
                f" {self.telegram_message_parser.call(item.name)}"
                f" x{item.quantity} "
                f"{self.telegram_message_parser.call('(')}"
                f"{self.telegram_message_parser.call(item.variant_name)}"
                f"{self.telegram_message_parser.call(')')}\n"
            )
        message += "\n"

        if order_data.is_local_pickup:
            message += f"✨ *Iran por él 🏠🚶🏼‍♂️*\n"
        else:
            message += f"✨ *Lo Enviamos 🚚📦*\n"

        reply_markup = {
            "inline_keyboard": [
                [
                    {
                        "text": "📦 Shopify Admin",
                        "url": f"{settings.SHOPIFY_ADMIN_URL}/orders/{order_data.order_id}",
                    }
                ]
            ]
        }
        self.telegram_service.send_message(
            message,
            message_thread_id=settings.TELEGRAM_ORDERS_MESSAGE_THREAD_ID,
            reply_markup=reply_markup,
        )


class CalendarChatMessageService:
    calendar_service = GoogleCalendarService()
    telegram_service = telegram_service

    def __init__(self, telegram_message_parser=None):
        super().__init__()
        self.telegram_message_parser = telegram_message_parser

    def notify_today_events(self, use_cache=False):
        logger.info("Notifying calendar events.")

        # Get the Hermosillo timezone
        hermosillo = pytz.timezone("America/Hermosillo")
        now = datetime.now(hermosillo)
        today = now.date()
        events: list[dict]
        if use_cache:
            events = self.calendar_service.get_events_from_cache(today)
        else:
            events: list[dict] = self.calendar_service.fetch_events(today)
        if not events:
            logger.info("No events found.")
            return
        message = "📅 *Eventos de Hoy* 📅\n\n"
        for event in events:
            start = datetime.fromisoformat(
                event.get("start", {}).get("dateTime", "")
            ).strftime("%I:%M %p")
            end = datetime.fromisoformat(
                event.get("end", {}).get("dateTime", "")
            ).strftime("%I:%M %p")
            summary = event.get("summary", "")
            message += f"> 🕒 *{start} \\- {end}* \\- {self.telegram_message_parser.call(summary)}\n"
        self.telegram_service.send_message(message)
