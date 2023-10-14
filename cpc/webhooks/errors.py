from cpc.app.errors import APIException


class WebhookException(APIException):
    status_code = 400
    default_code = "webhook_error"
    default_detail = "Error while processing webhook"
