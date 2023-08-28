import os

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', None)
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', None)

if TELEGRAM_BOT_TOKEN is None:
    raise AssertionError('TELEGRAM_BOT_TOKEN is not set')
if TELEGRAM_CHAT_ID is None:
    raise AssertionError('TELEGRAM_CHAT_ID is not set')

TELEGRAM_MENTIONS = os.getenv('TELEGRAM_MENTIONS', None)
if TELEGRAM_MENTIONS is not None:
    TELEGRAM_MENTIONS = TELEGRAM_MENTIONS.split(',')
else:
    TELEGRAM_MENTIONS = []
