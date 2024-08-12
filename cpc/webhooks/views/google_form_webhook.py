import logging

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from cpc.app.services.telegram import TelegramService, TelegramMessageParser
from cpc.network.decorators import log_raw_json
from cpc.webhooks.errors import WebhookException
from cpc.webhooks.serializers.google_form_input_serializer import (
    GoogleFormInputSerializer,
)
from cpc.webhooks.services.gform.submissions import FeedbackSubmission, LedgerSubmission

logger = logging.getLogger(__name__)


class GoogleFormWebhookView(APIView):
    serializer_class = GoogleFormInputSerializer
    submissions = {
        "feedback": FeedbackSubmission,
        "ledger": LedgerSubmission,
    }

    telegram_service = TelegramService(settings.TELEGRAM_BOT_TOKEN)
    telegram_message_parser = TelegramMessageParser()

    @log_raw_json
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        token = request.query_params.get("token")

        if token != settings.WEBHOOK_TOKEN:
            raise WebhookException("Invalid token", status_code=401)
        if serializer.is_valid(raise_exception=False) is False:
            raise WebhookException("Invalid data", status_code=400)

        data_type = serializer.validated_data.get("type")
        submission_type_class = self.submissions.get(data_type, None)
        if submission_type_class is None:
            raise WebhookException("Invalid submission type")

        logger.info(f"Processing {data_type} submission")

        try:
            submission = submission_type_class()
            setattr(submission, "telegram_service", self.telegram_service)
            setattr(submission, "telegram_message_parser", self.telegram_message_parser)
        except Exception as e:
            logger.exception(e)
            raise WebhookException("Error processing submission")

        submission.process(serializer.validated_data.get("data"))

        return Response(status=200)
