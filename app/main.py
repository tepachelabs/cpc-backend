import logging
from datetime import datetime

from flask import Flask, request, jsonify

from app import settings
from app.errors import WebhookException
from app.services.gform.gform import google_forms_webhook

app = Flask(__name__)

logger = logging.getLogger(__name__)


@app.route("/")
def hello_world():
    return f"<p>Tepache Labs {datetime.now().year}</p>"


@app.route("/gform/", methods=["POST"])
def google_form_webhook():
    token = request.args.get("token")

    if token == settings.WEBHOOK_TOKEN:
        data = request.json
        try:
            google_forms_webhook.process(data)
        except WebhookException as e:
            logger.error("Error while processing webhook", exc_info=e)
            response = {"message": "Webhook received, not parsed correctly"}
            return jsonify(response), 400

        response = {"message": "Webhook received successfully"}
        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid token"}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, threaded=True)
