import unittest
from unittest.mock import MagicMock, patch

from app import settings

class TestFeedbackSubmission(unittest.TestCase):

    def setUp(self):
        from app.services.gform.submissions import FeedbackSubmission
        self.telegram_service = MagicMock()
        self.submission = FeedbackSubmission(self.telegram_service)
        settings.TELEGRAM_MENTIONS = ["test_user"]

    def test_process(self):
        data = {
            "responses": {
                "What did you like about our service?": "I liked the fast response times.",
                "What could we improve?": "I think the UI could be more user-friendly.",
                "This is another question": ["This is another answer"],
                "This is yet another question": ["This is yet another answer", "Copy that"],
            }
        }
        self.telegram_service.parse_text.side_effect = lambda x: x
        self.submission.process(data)
        self.telegram_service.send_message.assert_called_once_with(
            "📝 *Completado: Valoramos tu opinión para mejorar* ✨\n\n"
            "*What did you like about our service?:*\nI liked the fast response times.\n\n"
            "*What could we improve?:*\nI think the UI could be more user-friendly.\n\n"
            "*This is another question:*\nThis is another answer\n\n"
            "*This is yet another question:*\nThis is yet another answer, Copy that\n\n"
            "*CC:*\n[@test_user](tg://user?id=test_user)"
        )