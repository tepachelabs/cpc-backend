import os

from app.services.gform.submissions import FeedbackSubmission
from app.services.telegram import telegram_service

WEBHOOK_TOKEN = os.getenv("WEBHOOK_TOKEN", None)

if WEBHOOK_TOKEN is None:
    raise AssertionError("WEBHOOK_TOKEN is not set")

SUBMISSION_CONFIG = {
    "feedback": FeedbackSubmission(telegram_service),
}
