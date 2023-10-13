import logging

from app.errors import WebhookException
from app.services.telegram import TelegramSubmission, telegram_submissions

logger = logging.getLogger(__name__)


class GoogleFormsWebhook:
    def __init__(self, config: TelegramSubmission) -> None:
        super().__init__()
        self._config = config

    def process(self, data: dict):
        data_type = data.get("type", None)
        submission_type = self._config.get(data_type, None)
        if submission_type is None:
            raise WebhookException("Invalid submission type")
        webhook_data = data.get("data", None)
        if webhook_data is None:
            raise WebhookException("Invalid webhook data")
        logger.info(f"Processing {data_type} submission")
        submission_type.process(webhook_data)


google_forms_webhook = GoogleFormsWebhook(config=telegram_submissions)
