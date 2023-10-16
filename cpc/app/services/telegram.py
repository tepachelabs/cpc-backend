from typing import Union, Optional

from telegram import Bot
from telegram.constants import ParseMode

from cpc import settings


class MarkdownV2Parser:
    @staticmethod
    def parse(text):
        special_characters = [
            "_",
            "*",
            "[",
            "]",
            "(",
            ")",
            "~",
            "`",
            ">",
            "#",
            "+",
            "-",
            "=",
            "|",
            "{",
            "}",
            ".",
            "!",
        ]

        for char in special_characters:
            text = text.replace(char, "\\" + char)

        return text


class TelegramService:
    def __init__(self, bot_token=None) -> None:
        super().__init__()
        self._bot = Bot(token=bot_token)
        self._parse_mode_config = {ParseMode.MARKDOWN_V2: MarkdownV2Parser.parse}

    def send_message(
        self,
        message: str,
        chat_id: Union[int, str] = settings.TELEGRAM_CHAT_ID,
        message_thread_id: Optional[int] = None,
        parse_mode=ParseMode.MARKDOWN_V2,
    ):
        import asyncio

        loop = asyncio.new_event_loop()
        loop.run_until_complete(
            self._bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=parse_mode,
                message_thread_id=message_thread_id,
            )
        )
        loop.close()

    def parse_text(self, text, parse_mode=ParseMode.MARKDOWN_V2):
        if parse_mode in self._parse_mode_config:
            return self._parse_mode_config[parse_mode](text)
        return text
