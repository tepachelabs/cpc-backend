import json
import logging
import os
from datetime import datetime

from django.core.cache import cache
from google.oauth2 import service_account
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)


class GoogleCalendarServiceBuilder:
    key = os.environ.get("GOOGLE_CALENDAR_API_JSON", None)

    def build(self):
        if self.key is None:
            return None

        json_key = json.loads(self.key)
        credentials = service_account.Credentials.from_service_account_info(json_key)
        return build("calendar", "v3", credentials=credentials)


class GoogleCalendarService:
    service = GoogleCalendarServiceBuilder().build()
    calendar_id = os.environ.get("GOOGLE_CALENDAR_ID", None)

    @staticmethod
    def key(day: datetime.date):
        return f'calendar:{day.strftime("%Y-%m-%d")}Z'

    def fetch_events(self, date: datetime.date):
        start_time = (
            datetime(date.year, date.month, date.day, 0, 0, 0).isoformat() + "-07:00"
        )
        end_time = (
            datetime(date.year, date.month, date.day, 23, 59, 59)
        ).isoformat() + "-07:00"

        logger.info(f"Fetching events from {start_time} to {end_time}")

        events_result = (
            self.service.events()
            .list(
                calendarId=self.calendar_id,
                timeMin=start_time,
                timeMax=end_time,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        return events_result.get("items", [])

    def get_calendar_events(self, day):
        events = self.get_events_from_cache(day)
        if not events:
            events = self.fetch_and_cache_events(day)
        return events

    def get_events_from_cache(self, day: datetime.date):
        key = self.key(day)
        events = cache.get(key)
        return events

    def cache_events(self, day: datetime.date):
        events = self.fetch_events(day)
        key = self.key(day)
        cache.set(key, events, timeout=86400)  # 24 hours TTL

    def fetch_and_cache_events(self, day):
        events = self.fetch_events(day)
        self.cache_events(day)
        return events
