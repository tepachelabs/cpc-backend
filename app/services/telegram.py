import asyncio

loop = asyncio.get_event_loop()

from telegram import Bot
from telegram.constants import ParseMode

from app import settings


class TelegramService:

    def __init__(self) -> None:
        super().__init__()
        if settings.TELEGRAM_BOT_TOKEN is None:
            raise Exception('TELEGRAM_BOT_TOKEN is not set')
        if settings.TELEGRAM_CHAT_ID is None:
            raise Exception('TELEGRAM_CHAT_ID is not set')

        self._bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        self._chat_id = settings.TELEGRAM_CHAT_ID

    def send_message(self, message: str):
        loop.run_until_complete(
            self._bot.send_message(chat_id=self._chat_id, text=message, parse_mode=ParseMode.MARKDOWN)
        )


telegram_service = TelegramService()
