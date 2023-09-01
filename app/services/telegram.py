from app import settings
from telegram import Bot

from telegram.constants import ParseMode
import asyncio

loop = asyncio.get_event_loop()


class TelegramService:
    def __init__(self) -> None:
        super().__init__()
        self._bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        self._chat_id = settings.TELEGRAM_CHAT_ID

    def send_message(self, message: str, parse_mode=ParseMode.MARKDOWN_V2):
        loop.run_until_complete(
            self._bot.send_message(
                chat_id=self._chat_id, text=message, parse_mode=parse_mode
            )
        )


telegram_service = TelegramService()
