import unittest
from unittest.mock import MagicMock

from cpc import settings


class TestLedgerSubmission(unittest.TestCase):
    def setUp(self):
        from cpc.webhooks.services.gform.submissions import LedgerSubmission

        self.telegram_service = MagicMock()
        self.telegram_message_parser = MagicMock()
        self.telegram_message_parser.call.side_effect = lambda x: x
        self.submission = LedgerSubmission(
            self.telegram_service, self.telegram_message_parser
        )

    def test_process(self):
        data = {
            "responses": {
                "This is another question": "This is another answer",
                "This is another another question": ["This is another another answer"],
                "This is another another another question": "*hello there*",
            }
        }
        self.telegram_service.parse_text.side_effect = lambda x: x
        self.submission.process(data)
        self.telegram_service.send_message.assert_called_once_with(
            "📝 *Compra interna realizada* 💸💸\n\n"
            "*This is another question:*\nThis is another answer\n\n"
            "*This is another another question:*\nThis is another another answer\n\n"
            "*This is another another another question:*\n*hello there*\n\n",
            message_thread_id=None,
        )


class TestFeedbackSubmission(unittest.TestCase):
    def setUp(self):
        from cpc.webhooks.services.gform.submissions import FeedbackSubmission

        self.telegram_service = MagicMock()
        self.telegram_message_parser = MagicMock()
        self.telegram_message_parser.call.side_effect = lambda x: x
        self.submission = FeedbackSubmission(
            self.telegram_service, self.telegram_message_parser
        )
        settings.TELEGRAM_MENTIONS = ["test_user"]

    def test_process(self):
        data = {
            "responses": {
                "What did you like about our service?": "I liked the fast response times.",
                "What could we improve?": "I think the UI could be more user-friendly.",
                "This is another question": ["This is another answer"],
                "This is yet another question": [
                    "This is yet another answer",
                    "Copy that",
                ],
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

    def test_process__with_email(self):
        data = {
            "email": "foo@test.email",
            "responses": {
                "What did you like about our service?": "I liked the fast response times.",
            },
        }
        self.telegram_service.parse_text.side_effect = lambda x: x
        self.submission.process(data)
        self.telegram_service.send_message.assert_called_once_with(
            "📝 *Completado: Valoramos tu opinión para mejorar* ✨\n\n"
            "*Email:*\nfoo@test.email\n\n"
            "*What did you like about our service?:*\nI liked the fast response times.\n\n"
            "*CC:*\n[@test_user](tg://user?id=test_user)"
        )
