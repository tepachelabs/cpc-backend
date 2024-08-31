import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", None)
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", None)
TELEGRAM_LEDGER_MESSAGE_THREAD_ID = os.getenv("TELEGRAM_LEDGER_MESSAGE_THREAD_ID", None)
TELEGRAM_ORDERS_MESSAGE_THREAD_ID = os.getenv("TELEGRAM_ORDERS_MESSAGE_THREAD_ID", None)

TELEGRAM_MENTIONS = os.getenv("TELEGRAM_MENTIONS", None)
if TELEGRAM_MENTIONS is not None:
    TELEGRAM_MENTIONS = TELEGRAM_MENTIONS.split(",")
else:
    TELEGRAM_MENTIONS = []
