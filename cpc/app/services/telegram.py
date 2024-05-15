from typing import Union, Optional

import requests

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


class TelegramService:
    def __init__(self, bot_token=None) -> None:
        super().__init__()
        self._bot_token = bot_token
        self._parse_mode_config = {"MarkdownV2": MarkdownV2Parser.parse}

    def send_message(
        self,
        message: str,
        chat_id: Union[int, str] = settings.TELEGRAM_CHAT_ID,
        message_thread_id: Optional[int] = None,
        parse_mode="MarkdownV2",
    ):
        url = f"https://api.telegram.org/bot{self._bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": parse_mode,
            "message_thread_id": message_thread_id,
        }
        response = requests.post(url, data=data)
        if response.status_code != 200:
            raise Exception(f"Failed to send message: {response.text}")
        return response.json()

    # TODO: Move this out.
    def parse_text(self, text, parse_mode="MarkdownV2"):
        text = str(text)
        if parse_mode in self._parse_mode_config:
            return self._parse_mode_config[parse_mode](text)
        return text


telegram_service = TelegramService(settings.TELEGRAM_BOT_TOKEN)
