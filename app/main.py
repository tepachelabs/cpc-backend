from datetime import datetime

from flask import Flask, request, jsonify
from app import settings
from app.services.telegram import telegram_service

app = Flask(__name__)


@app.route("/")
def hello_world():
    return f"<p>Tepache Labs {datetime.now().year}</p>"


@app.route('/telegram/feedback', methods=['POST'])
def webhook():
    token = request.args.get('token')

    if token == settings.WEBHOOK_TOKEN:
        data = request.json
        responses = data.get('responses', None)
        if responses is None:
            response = {'message': 'Webhook received successfully'}
            return jsonify(response), 202

        text = f"📝 *Completado: Valoramos tu opinión para mejorar* ✨\n\n"
        for question, answer in responses.items():
            if answer == '':
                text += f"*{question}:*\nNo nos has dejado ningún comentario o recomendación\\."
            else:
                text += f"*{question}:*\n{answer}"
            text += '\n\n'
        mentions = []
        for mention in settings.TELEGRAM_MENTIONS:
            split_mention = mention.split('@')
            if len(split_mention) > 1:
                mentions.append(f"[@{split_mention[0]}](tg://user?id={split_mention[1]})")
            else:
                mentions.append(f"[@{mention}](tg://user?id={mention})")

        if len(mentions) > 0:
            text += '*CC:*\n'
            text += ', '.join(mentions)

        telegram_service.send_message(text)

        response = {'message': 'Webhook received successfully'}
        return jsonify(response), 200
    else:
        return jsonify({'message': 'Invalid token'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, threaded=True)
