import asyncio
import logging

from django.conf import settings
from django.core.management import BaseCommand
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

from cpc.celery import app as celery_app

logger = logging.getLogger()


class Command(BaseCommand):
    help = "Run Telegram Bot"

    @staticmethod
    async def inventory_reminder_handler(_update: Update, _context: CallbackContext):
        # Keep it as a celery task as the cron job is already set up
        celery_app.send_task("cpc.shopify_backend.tasks.inventory_reminder")

    @staticmethod
    async def post_init(application):
        inventario_command = BotCommand("inventario", "Recordatorio de inventario")
        await application.bot.set_my_commands(commands=[inventario_command])

    def handle(self, *args, **options):
        if settings.TELEGRAM_BOT_TOKEN is None:
            logger.error("TELEGRAM_BOT_TOKEN is not set in the environment variables.")
            return

        start_handler = CommandHandler("inventario", self.inventory_reminder_handler)

        application = (
            ApplicationBuilder()
            .token(settings.TELEGRAM_BOT_TOKEN)
            .post_init(self.post_init)
            .build()
        )
        application.add_handler(start_handler)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(application.run_polling())
