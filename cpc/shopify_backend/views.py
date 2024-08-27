import logging
import base64
import hashlib
import hmac

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from cpc.shopify_backend.errors import ShopifyWebhookException
from cpc.shopify_backend.services import OrderCreateWebhookService
from django.conf import settings

logger = logging.getLogger(__name__)


class APIWebhookView(APIView):
    header_topic = "x-shopify-topic"
    header_hmac = "x-shop-hmac-sha256"
    shopify_webhook_secret = settings.SHOPIFY_WEBHOOK_SECRET

    def verify_webhook(self, request):
        hmac_header = request.headers.get(self.header_hmac)
        if not hmac_header:
            return False
        body = request.body
        secret = self.shopify_webhook_secret.encode("utf-8")
        sha256hash = hmac.new(secret, body, hashlib.sha256)
        calculated_hmac = base64.b64encode(sha256hash.digest()).decode("utf-8")
        return hmac.compare_digest(calculated_hmac, hmac_header)


class AdminWebhookView(APIWebhookView):
    def post(self, request):
        if not self.verify_webhook(request):
            return Response(
                {"message": "forbidden request"}, status=status.HTTP_403_FORBIDDEN
            )

        topic = request.headers.get(self.header_topic)
        service = self._get_service(topic)
        if service is None:
            return Response({"message": "Invalid topic"}, status=400)
        data = request.data
        try:
            service.process(data)
        except ShopifyWebhookException as e:
            logger.error(
                f"Error processing webhook: {str(e)}",
                exc_info=True,
                extra={"data": data},
            )
            return Response({"message": str(e)}, status=500)
        return Response({"message": f"Webhook '{topic}' processed", "data": data})

    @staticmethod
    def _get_service(topic):
        if topic == "orders/create":
            return OrderCreateWebhookService()
        return None
