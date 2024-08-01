from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from cpc.app.services.chat_messages import CalendarChatMessageService
from cpc.app.services.telegram import TelegramMessageParser
from cpc.celery import app as celery_app


class BaseCommand:
    command_name = None

    async def handler(self, _update: Update, _context: CallbackContext):
        raise NotImplementedError

    def command_handler(self) -> CommandHandler:
        return CommandHandler(self.command_name, self.handler)


class InventarioCommand(BaseCommand):
    command_name = "inventario"
    command_description = "Verificar inventario en Shopify POS"
    task_executor = celery_app

    async def handler(self, _update: Update, _context: CallbackContext):
        # Keep it as a celery task as the cron job is already set up
        self.task_executor.send_task("cpc.shopify_backend.tasks.inventory_reminder")


class EventosCommand(BaseCommand):
    command_name = "eventos"
    command_description = "Verificar eventos de hoy de Google Calendar"

    async def handler(self, _update: Update, _context: CallbackContext):
        calendar_message_service = CalendarChatMessageService(
            telegram_message_parser=TelegramMessageParser()
        )
        calendar_message_service.notify_today_events()
