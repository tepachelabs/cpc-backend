import logging
from datetime import datetime

import pytz

from cpc.app.services import GoogleCalendarService
from cpc.app.services.telegram import telegram_service

logger = logging.getLogger(__name__)


class CalendarChatMessageService:
    calendar_service = GoogleCalendarService()

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
        telegram_service.send_message(message)
