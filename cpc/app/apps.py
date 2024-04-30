import asyncio

from django.apps import AppConfig
from django.conf import settings

from cpc.app.services.telegram import TelegramService


class CpcAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cpc.app"

    def ready(self):
        super().ready()
