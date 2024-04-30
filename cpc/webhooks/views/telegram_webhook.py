import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update, Bot
from telegram.ext import Updater

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dispatcher = Updater(bot, update_queue=None)


@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        json_string = request.body.decode("UTF-8")
        update = Update.de_json(json.loads(json_string), bot)
        dispatcher.process_update(update)
    return JsonResponse({"ok": "POST request processed"})
