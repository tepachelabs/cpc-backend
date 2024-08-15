import asyncio
import logging

from django.conf import settings
from telegram import BotCommand
from telegram.ext import ApplicationBuilder, Application

from cpc.app.telegram.commands import InventarioCommand, EventosCommand

logger = logging.getLogger()


class TelegramBot:
    BOT_COMMANDS = [
        InventarioCommand(),
        EventosCommand(),
    ]

    @staticmethod
    async def post_init(application: Application):
        if hasattr(application, "bot"):
            await application.bot.set_my_commands(
                commands=[
                    BotCommand(command.command_name, command.command_description)
                    for command in TelegramBot.BOT_COMMANDS
                ]
            )
            logger.info("Bot post init completed")
        else:
            logger.error("Bot is not initialized in the application")

    def start(self):
        if settings.TELEGRAM_BOT_TOKEN is None:
            logger.error("TELEGRAM_BOT_TOKEN is not set in the environment variables")
            return

        application = (
            ApplicationBuilder()
            .token(settings.TELEGRAM_BOT_TOKEN)
            .post_init(self.post_init)
            .build()
        )

        # Add all commands to the bot
        for command in TelegramBot.BOT_COMMANDS:
            application.add_handler(command.command_handler())

        loop = asyncio.get_event_loop()
        # TODO Should we refactor this to use a webhook instead of polling?
        loop.run_until_complete(application.run_polling())
