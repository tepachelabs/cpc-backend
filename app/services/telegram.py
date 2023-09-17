from app import settings
from telegram import Bot

from telegram.constants import ParseMode
import asyncio

loop = asyncio.get_event_loop()


class MarkdownV2Parser:
    @staticmethod
    def parse(text):
        special_characters = ['_',
                              '*',
                              '[',
                              ']',
                              '(',
                              ')',
                              '~',
                              '`',
                              '>',
                              '#',
                              '+',
                              '-',
                              '=',
                              '|',
                              '{',
                              '}',
                              '.',
                              '!']

        for char in special_characters:
            text = text.replace(char, '\\' + char)

        return text


class TelegramService:
    def __init__(self) -> None:
        super().__init__()
        self._bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        self._chat_id = settings.TELEGRAM_CHAT_ID
        self._text_to_parse = {
            ParseMode.MARKDOWN_V2: MarkdownV2Parser.parse
        }

    def send_message(self, message: str, parse_mode=ParseMode.MARKDOWN_V2):
        if parse_mode in self._text_to_parse:
            message = self._text_to_parse[parse_mode](message)

        loop.run_until_complete(
            self._bot.send_message(
                chat_id=self._chat_id, text=message, parse_mode=parse_mode
            )
        )


telegram_service = TelegramService()
