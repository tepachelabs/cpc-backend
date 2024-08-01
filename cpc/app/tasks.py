import logging
from ssl import SSLEOFError

from celery import shared_task

from cpc.app.services.chat_messages import CalendarChatMessageService
from cpc.app.services.telegram import TelegramMessageParser

logger = logging.getLogger()

ERRORS_TO_RETRY = (SSLEOFError,)


@shared_task(
    autoretry_for=ERRORS_TO_RETRY, retry_kwargs={"max_retries": 5, "countdown": 60}
)
def notify_calendar_events():
    calendar_message_service = CalendarChatMessageService(
        telegram_message_parser=TelegramMessageParser()
    )
    calendar_message_service.notify_today_events()
