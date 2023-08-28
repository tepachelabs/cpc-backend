import os

WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN', None)

if WEBHOOK_TOKEN is None:
    raise AssertionError('WEBHOOK_TOKEN is not set')