from typing import Union, Optional

from telegram import Update
from telegram.ext import Application, CommandHandler
from telegram.constants import ParseMode
from telegram.ext import Updater

from cpc import settings


class MarkdownV2Parser:
    @staticmethod
    def parse(text: str):
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


# TODO Refactor this entire class and usages, its so stupid.
class TelegramService:
    def __init__(self, bot_token=None) -> None:
        super().__init__()
        self._application = Application.builder().token(bot_token).build()
        self._parse_mode_config = {ParseMode.MARKDOWN_V2: MarkdownV2Parser.parse}

    async def add_commands(self):
        await self._application.bot.set_my_commands([("conteo", "Conteo de productos")])
        await self._application.initialize()
        await self._application.start()
        await self._application.updater.start_polling(allowed_updates=Update.ALL_TYPES)

    async def send_message(
        self,
        message: str,
        chat_id: Union[int, str] = settings.TELEGRAM_CHAT_ID,
        message_thread_id: Optional[int] = None,
        parse_mode=ParseMode.MARKDOWN_V2,
    ):
        await self._application.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode=parse_mode,
            message_thread_id=message_thread_id,
        )

    # TODO: Move this out.
    def parse_text(self, text, parse_mode=ParseMode.MARKDOWN_V2):
        text = str(text)
        if parse_mode in self._parse_mode_config:
            return self._parse_mode_config[parse_mode](text)
        return text
