import logging
from abc import ABC, abstractmethod

from cpc import settings
from cpc.webhooks.errors import WebhookException

from cpc.app.services.telegram import TelegramService, TelegramMessageParser

logger = logging.getLogger(__name__)


class GoogleFormSubmission(ABC):
    @abstractmethod
    def process(self, data: dict):
        raise NotImplementedError


class FeedbackSubmission(GoogleFormSubmission):
    """
    {
        "type": "feedback",
        data: {
            "responses": dict[str,str]
        }
    }
    """

    def __init__(
        self,
        telegram_service: TelegramService,
        telegram_message_parser: TelegramMessageParser,
    ) -> None:
        super().__init__()
        self.telegram_service = telegram_service
        self.telegram_message_parser = telegram_message_parser

    def process(self, data: dict):
        responses = data.get("responses", None)
        if responses is None:
            raise WebhookException("Invalid responses")

        text = f"📝 *Completado: Valoramos tu opinión para mejorar* ✨\n\n"
        for question, answer in responses.items():
            if isinstance(answer, list):
                answer = ", ".join(answer)
            if answer == "" or len(answer) == 0:
                text += f"*{question}:*\nNo nos has dejado ningún comentario o recomendación\\."
            else:
                text += f"*{question}:*\n{self.telegram_message_parser.call(answer)}"
            text += "\n\n"
        mentions = []
        for mention in settings.TELEGRAM_MENTIONS:
            split_mention = mention.split("@")
            if len(split_mention) > 1:
                mentions.append(
                    f"[@{split_mention[0]}](tg://user?id={split_mention[1]})"
                )
            else:
                mentions.append(f"[@{mention}](tg://user?id={mention})")

        if len(mentions) > 0:
            text += "*CC:*\n"
            text += ", ".join(mentions)

        self.telegram_service.send_message(text)


class LedgerSubmission(GoogleFormSubmission):
    """
    {
        "type": "ledger",
        data: {
            "responses": dict[str,str]
        }
    }
    """

    def __init__(
        self,
        telegram_service: TelegramService,
        telegram_message_parser: TelegramMessageParser,
    ) -> None:
        super().__init__()
        self.telegram_service = telegram_service
        self.telegram_message_parser = telegram_message_parser
        self.message_thread_id = settings.TELEGRAM_LEDGER_MESSAGE_THREAD_ID

    def process(self, data: dict):
        responses = data.get("responses", None)
        if responses is None:
            raise WebhookException("Invalid responses")

        text = f"📝 *Compra interna realizada* 💸💸\n\n"
        for question, answer in responses.items():
            if type(answer) == list:
                answer = ", ".join(answer)
            text += f"*{question}:*\n{self.telegram_message_parser.call(answer)}"
            text += "\n\n"

        self.telegram_service.send_message(
            text, message_thread_id=self.message_thread_id
        )
