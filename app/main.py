from flask import Flask, request, jsonify
from app import settings
from app.services.telegram import telegram_service

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>!</p>"


@app.route('/telegram/feedback', methods=['POST'])
def webhook():
    token = request.args.get('token')

    if settings.WEBHOOK_TOKEN is None:
        raise Exception('WEBHOOK_TOKEN is not set')

    if token == settings.WEBHOOK_TOKEN:
        data = request.json
        feedback_message = data['feedback_message']
        text = f"*Nos interesa saber tu opinion:*\n{feedback_message}"
        telegram_service.send_message(text)
        response = {'message': 'Webhook received successfully'}
        return jsonify(response), 200
    else:
        return jsonify({'message': 'Invalid token'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, threaded=True)
