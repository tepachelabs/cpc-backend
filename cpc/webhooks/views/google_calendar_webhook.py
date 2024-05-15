from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# TODO: Finish up!
@csrf_exempt
def google_calendar_webhook(request):
    # This webhook is received when there is a change in Google Calendar
    # we still need to go and call the Calendar events API to get the actual event
    # and then process it.
    #
    # The bot will work in a daily basis so, we can just store the entire calendar day at the beginning of the day
    # Post events to Telegram if there is a change on the day.
    if request.method == "POST":
        all_headers = request.headers
        # Print all headers
        print("All Headers:")
        for header_name, header_value in all_headers.items():
            print(f"{header_name}: {header_value}")
    return JsonResponse({"ok": "POST request processed"})
