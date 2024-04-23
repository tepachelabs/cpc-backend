import asyncio

from django.apps import AppConfig
from django.conf import settings

from cpc.app.services.telegram import TelegramService


class CpcAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cpc.app"

    def ready(self):
        super().ready()

        # TODO Refactor this remove it from here
        telegram = TelegramService(settings.TELEGRAM_BOT_TOKEN)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(telegram.add_commands())
        finally:
            loop.close()
