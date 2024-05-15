import logging
import os
import uuid

from cpc.app.services.google import GoogleCalendarServiceBuilder

logger = logging.getLogger(__name__)


class RegisterGoogleCalendarWebhookService:
    service = GoogleCalendarServiceBuilder().build()
    calendar_id = os.environ.get("GOOGLE_CALENDAR_ID", None)
    base_url = os.environ.get("BASE_URL", None)
    webhook_token = os.environ.get("WEBHOOK_TOKEN", None)

    def call(self):
        if self.service is None or self.calendar_id is None:
            logger.info("Google Calendar webhook not registered.")
            return

        webhook_url = f"{self.base_url}/webhooks/google/calendar"
        subscription_id = uuid.uuid4().hex
        subscription_body = {
            "id": subscription_id,
            "type": "web_hook",
            "address": webhook_url,
            "token": self.webhook_token,
            "params": {
                "ttl": "82800"  # 23 hours, so from 11-12pm we can refresh the subscription without having it twice.
            },
        }

        self.service.events().watch(
            calendarId=self.calendar_id, body=subscription_body
        ).execute()
