import logging
from datetime import datetime

import pytz
from celery import shared_task

from cpc.app.services.telegram import telegram_service
from cpc.app.services import GoogleCalendarService

logger = logging.getLogger()


@shared_task
def notify_calendar_events():
    logger.info("Notifying calendar events.")
    # Get the Hermosillo timezone
    hermosillo = pytz.timezone("America/Hermosillo")
    now = datetime.now(hermosillo)
    today = now.date()

    events: list[dict] = GoogleCalendarService().get_calendar_events(today)
    if not events:
        logger.info("No events found.")
        return
    message = "📅 *Eventos de Hoy* 📅\n\n"
    for event in events:
        start = datetime.fromisoformat(
            event.get("start", {}).get("dateTime", "")
        ).strftime("%I:%M %p")
        end = datetime.fromisoformat(event.get("end", {}).get("dateTime", "")).strftime(
            "%I:%M %p"
        )
        summary = event.get("summary", "")
        message += (
            f"> 🕒 *{start} \\- {end}* \\- {telegram_service.parse_text(summary)}\n"
        )
    telegram_service.send_message(message)
