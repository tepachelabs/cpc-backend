import logging
import os
from datetime import datetime

from huey import MemoryHuey, crontab

from cpc.app.services.telegram import TelegramService

logger = logging.getLogger(__name__)

huey = MemoryHuey()


@huey.periodic_task(crontab(minute=0, hour=7))
def task_test():
    telegram_service = TelegramService(os.getenv("TELEGRAM_BOT_TOKEN"))
    telegram_service.send_message(
        "Hello there", chat_id=os.getenv("TEST_TELEGRAM_CHAT_ID")
    )
    logger.info(f"test: {datetime.now()}")
