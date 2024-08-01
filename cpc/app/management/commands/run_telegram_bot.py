import logging

from django.core.management import BaseCommand

from cpc.app.telegram.bot import TelegramBot

logger = logging.getLogger()


class Command(BaseCommand):
    help = "Run Telegram Bot"
    bot = TelegramBot()

    def handle(self, *args, **options):
        self.bot.start()
